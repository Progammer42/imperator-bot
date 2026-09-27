"""
Der Imperator Bot - fuehrt "Orders" gegen festgelegte Personen/Rollen aus.
Befehle:
  !executeorder1, !executeorder2, ...  -> feste Orders aus config.py
  !executerandomorder                  -> fuehrt eine zufaellige Order aus
Nur Nutzer mit der Rolle ALLOWED_ROLE_NAME (siehe config.py) duerfen die Befehle benutzen.
"""

import os
import json
import random
import asyncio
import datetime
import discord
from discord.ext import commands

from config import ALLOWED_ROLE_NAME, ORDERS

# --- Bot-Setup ---
intents = discord.Intents.default()
intents.members = True          # noetig, um Mitglieder zu bannen/timeouten
intents.message_content = True  # noetig, um Befehle wie !executeorder1 zu lesen

bot = commands.Bot(command_prefix="!", intents=intents)

# --- Statistik (wird in einer Datei gespeichert, damit sie einen Neustart ueberlebt) ---
STATS_FILE = "stats.json"


def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)


order_stats = load_stats()  # { "1": 3, "2": 1, ... }


def record_execution(order_number: int):
    key = str(order_number)
    order_stats[key] = order_stats.get(key, 0) + 1
    save_stats(order_stats)


# Emojis fuer die zufaellige Reaktion nach jeder ausgefuehrten Order
RANDOM_REACTIONS = ["⚡", "🔥", "💀", "😈", "🫡", "☠️", "🚨", "👑", "🎯", "🛑"]


def has_imperator_role(ctx: commands.Context) -> bool:
    return any(role.name == ALLOWED_ROLE_NAME for role in ctx.author.roles)


@bot.event
async def on_ready():
    print(f"Bot ist online als {bot.user}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("🚫 Du hast nicht die Berechtigung, diese Order auszuführen.")
    elif isinstance(error, commands.CommandNotFound):
        pass  # unbekannte Befehle einfach ignorieren
    else:
        await ctx.send(f"⚠️ Fehler: {error}")
        raise error


async def apply_action(member, action, reason, timeout_minutes):
    """Führt eine einzelne Aktion (timeout/ban) auf ein Mitglied aus."""
    if action == "timeout":
        until = discord.utils.utcnow() + datetime.timedelta(minutes=timeout_minutes)
        await member.timeout(until, reason=reason)
    elif action == "ban":
        await member.ban(reason=reason)


async def send_countdown(ctx):
    """Kleine dramatische Countdown-Nachricht vor jeder Order."""
    msg = await ctx.send("⚠️ Order wird ausgeführt in **3**...")
    await asyncio.sleep(1)
    await msg.edit(content="⚠️ Order wird ausgeführt in **2**...")
    await asyncio.sleep(1)
    await msg.edit(content="⚠️ Order wird ausgeführt in **1**...")
    await asyncio.sleep(1)
    await msg.edit(content="💥 Order wird jetzt ausgeführt!")


async def show_stats(ctx):
    """Zeigt die Statistik: wie oft wurde welche Order ausgeführt."""
    if not order_stats:
        await ctx.send("📊 Es wurde noch keine Order ausgeführt.")
        return

    lines = []
    for num_str, count in sorted(order_stats.items(), key=lambda x: int(x[0])):
        num = int(num_str)
        order = ORDERS.get(num)
        label = order.get("reason", f"Order {num}") if order else f"Order {num}"
        lines.append(f"Order {num} ({label}): **{count}x** ausgeführt")

    await ctx.send("📊 **Order-Statistik:**\n" + "\n".join(lines))


async def run_order(ctx: commands.Context, order_number: int, skip_countdown: bool = False):
    order = ORDERS.get(order_number)
    if order is None:
        await ctx.send(f"Order {order_number} ist nicht konfiguriert.")
        return

    action = order["action"]

    # --- Sonderfall: Statistik-Order ---
    if action == "stats":
        await show_stats(ctx)
        record_execution(order_number)
        return

    if action not in ("timeout", "ban"):
        await ctx.send(f"Unbekannte Aktion '{action}' für Order {order_number}.")
        return

    # Countdown vor jeder "echten" Order (Timeout/Ban)
    if not skip_countdown:
        await send_countdown(ctx)

    guild = ctx.guild
    reason = order.get("reason", f"Order {order_number}")
    timeout_minutes = order.get("timeout_minutes", 60)
    target = order.get("target", "user")  # "user" (Standard) oder "role"

    # --- Fall 1: Order zielt auf EINE einzelne Person (user_id) ---
    if target == "user":
        member = guild.get_member(order["user_id"])
        if member is None:
            try:
                member = await guild.fetch_member(order["user_id"])
            except discord.NotFound:
                await ctx.send("⚠️ Die Zielperson wurde auf diesem Server nicht gefunden.")
                return

        try:
            await apply_action(member, action, reason, timeout_minutes)
        except discord.Forbidden:
            await ctx.send(f"⚠️ Keine Berechtigung, um das bei {member.mention} auszuführen (Bot-Rolle muss über der Zielrolle stehen).")
            return

        if action == "timeout":
            await ctx.send(f"⏳ Order {order_number} ausgeführt: {member.mention} wurde für {timeout_minutes} Minuten in den Timeout geschickt.")
        else:
            await ctx.send(f"🔨 Order {order_number} ausgeführt: {member.mention} wurde gebannt.")

    # --- Fall 2: Order zielt auf ALLE mit einer bestimmten ROLLE ---
    elif target == "role":
        role_name = order.get("role_name")
        role = discord.utils.get(guild.roles, name=role_name)
        if role is None:
            await ctx.send(f"⚠️ Rolle '{role_name}' wurde auf diesem Server nicht gefunden.")
            return

        members = [m for m in role.members if not m.bot]
        if not members:
            await ctx.send(f"Niemand mit der Rolle '{role_name}' gefunden.")
            return

        erfolgreich = []
        fehlgeschlagen = []
        for member in members:
            try:
                await apply_action(member, action, reason, timeout_minutes)
                erfolgreich.append(member.display_name)
            except discord.Forbidden:
                fehlgeschlagen.append(member.display_name)

        verb = f"für {timeout_minutes} Minuten in den Timeout geschickt" if action == "timeout" else "gebannt"
        msg = f"Order {order_number} ausgeführt: {len(erfolgreich)} Person(en) mit Rolle '{role_name}' wurden {verb}."
        if erfolgreich:
            msg += "\n✅ " + ", ".join(erfolgreich)
        if fehlgeschlagen:
            msg += "\n⚠️ Fehlgeschlagen (keine Berechtigung): " + ", ".join(fehlgeschlagen)
        await ctx.send(msg)

    else:
        await ctx.send(f"Unbekanntes Ziel '{target}' für Order {order_number}.")
        return

    # Statistik hochzaehlen + zufaellige Reaktion, nur bei erfolgreicher Ausfuehrung
    record_execution(order_number)
    try:
        await ctx.message.add_reaction(random.choice(RANDOM_REACTIONS))
    except discord.HTTPException:
        pass


# Für jede Order in config.py wird automatisch ein Befehl !executeorderX erzeugt
def make_order_command(order_number: int):
    @commands.check(has_imperator_role)
    async def _cmd(ctx):
        await run_order(ctx, order_number)
    _cmd.__name__ = f"executeorder{order_number}"
    return _cmd


for num in ORDERS.keys():
    bot.command(name=f"executeorder{num}")(make_order_command(num))


# --- Zufalls-Order: fuehrt eine zufaellig ausgewaehlte Order aus ---
@bot.command(name="executerandomorder")
@commands.check(has_imperator_role)
async def executerandomorder(ctx):
    order_number = random.choice(list(ORDERS.keys()))
    await ctx.send(f"🎲 Zufallsorder gewählt: **Order {order_number}**")
    await run_order(ctx, order_number)


if __name__ == "__main__":
    TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
    if not TOKEN:
        raise RuntimeError(
            "Kein Bot-Token gefunden! Setze die Umgebungsvariable DISCORD_BOT_TOKEN."
        )
    bot.run(TOKEN)
