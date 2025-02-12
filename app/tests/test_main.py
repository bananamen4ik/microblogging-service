"""Test main module."""

import asyncio

import pytest


@pytest.mark.asyncio
async def test_t(client):
    await asyncio.sleep(10)
    assert True
