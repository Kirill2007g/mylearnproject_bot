from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage

from mylearnprojectbot.handlers.main_commands import cmd_add, match_re_search

PATCH_ADD_RECORD = "mylearnprojectbot.handlers.main_commands.add_record"

pytestmark = pytest.mark.asyncio


@pytest.fixture
def message():
    return AsyncMock()


@pytest.fixture
def state():
    key = StorageKey(bot_id=1, chat_id=1, user_id=1)
    return FSMContext(storage=MemoryStorage(), key=key)


@pytest.fixture
def mock_add_record():
    with patch(PATCH_ADD_RECORD, new_callable=AsyncMock) as mock:
        yield mock


def cmd(args):
    return CommandObject(prefix="/", command="add", args=args)


@pytest.mark.parametrize(
    "args",
    [
        "Математика; Геометрия; Оценка 5",
        "Математика;\nГеометрия;\nОценка 5",  # формат со скриншота
        "Математика\nГеометрия\nОценка 5",
        "  Математика ;Геометрия;  Оценка 5;  ",
    ],
)
async def test_add_valid_formats(message, state, mock_add_record, args):
    await cmd_add(message=message, state=state, command=cmd(args))

    data = await state.get_data()
    assert data["subject"] == "Математика"
    assert data["topic"] == "Геометрия"
    assert data["ration"] == "Оценка 5"
    assert isinstance(data["date"], datetime)

    mock_add_record.assert_awaited_once_with(data)
    message.answer_photo.assert_awaited_once()
    message.answer.assert_awaited_once_with("✅ Запись добавлена")


@pytest.mark.parametrize("args", [None, "", "Математика", "Математика; Геометрия"])
async def test_add_not_enough_fields(message, state, mock_add_record, args):
    await cmd_add(message=message, state=state, command=cmd(args))

    mock_add_record.assert_not_awaited()
    assert await state.get_data() == {}
    message.answer.assert_awaited_once_with("Нужно 3 поля: subject; topic; ration")


@pytest.mark.parametrize(
    "text, expected",
    [
        ("/show 2026-10-27", datetime(2026, 10, 27)),
        ("/show заметка 2025-01-05 ещё текст", datetime(2025, 1, 5)),
        ("/show без даты", None),
    ],
)
async def test_match_re_search(text, expected):
    assert await match_re_search(text) == expected


async def test_match_re_search_invalid_date():
    with pytest.raises(ValueError):
        await match_re_search("/show 2026-13-45")