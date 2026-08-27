# Lune database

import aiosqlite
import asyncio
from datetime import datetime
from backend.validation.schemas import Message, Session, Skill

DB_PATH = "backend/utils/lune_db.db"



async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        

        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                second_name TEXT,
                last_name TEXT NOT NULL,
                email TEXT,
                birth_date TEXT NOT NULL
            )
        """
        )

        await db.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                creation_date TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """
        )

        await db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                message_id TEXT PRIMARY KEY,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                time_sent TEXT NOT NULL,
                session_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            """
        )


        await db.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                skill_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                permissions_needed BOOL
            )
        """
        )
        
        await db.commit()


async def save_chat_turn(user: Message, assistant: Message) -> None:
                         async with aiosqlite.connect(DB_PATH) as db:
                            await db.executemany(
                                "INSERT INTO messages (message_id, role, content, time_sent, session_id, user_id) "
                                "VALUES (?, ?, ?, ?, ?, ?)",
                                [(user.message_id, user.role, user.content, user.time_sent, user.session_id, user.user_id),
                                 (assistant.message_id, assistant.role, assistant.content, assistant.time_sent, assistant.session_id, assistant.user_id)]
                                )
                            await db.commit()


async def load_chat_history(session_id: Session) -> list[Message]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT message_id, role, content, time_sent, session_id, user_id FROM messages WHERE session_id = ? ORDER BY time_sent ASC",
            (session_id.session_id,)
        )
        rows = await cursor.fetchall()
        await cursor.close()

    return [Message(message_id=row[0], role=row[1], content=row[2], time_sent=datetime.fromisoformat(row[3]), session_id=row[4], user_id=row[5]) for row in rows]


async def safe_save_chat_turn(user: Message, assistant: Message) -> None:
    try:
        await save_chat_turn(user, assistant)
    except Exception as e:
        raise Exception(f"Error saving chat turn: {e}")


async def safe_load_chat_history(session_id: Session) -> list[Message]:
    try:
        return await load_chat_history(session_id)
    except Exception as e:
        raise Exception(f"Error loading chat history: {e}")
