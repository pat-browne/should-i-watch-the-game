from email.message import EmailMessage
import smtplib

from winwatch.models import GameResult


def send_watch_email(
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    email_from: str,
    email_to: str,
    game: GameResult,
) -> None:
    msg = EmailMessage()
    msg["Subject"] = f"Watch alert: {game.team} won"
    msg["From"] = email_from
    msg["To"] = email_to
    msg.set_content(
        f"{game.team} beat {game.opponent} ({game.league}) on {game.game_time.isoformat()} UTC. You should watch the game."
    )

    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
