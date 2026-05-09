"""Tests for blender_mcp.utils.mesh_validator."""

import pytest
from blender_mcp.utils.mesh_validator import (
    validate_location,
    validate_mesh_name,
    validate_scale,
    validate_vertex_count,
)


class TestValidateMeshName:
    def test_valid_name(self):
        assert validate_mesh_name("Cube").valid is True

    def test_empty_name(self):
        result = validate_mesh_name("")
        assert not result
        assert "empty" in result.error.lower()

    def test_whitespace_only_name(self):
        assert not validate_mesh_name("   ")

    def test_name_too_long(self):
        result = validate_mesh_name("A" * 64)
        assert not result
        assert "63" in result.error

    def test_name_exactly_63_chars(self):
        assert validate_mesh_name("B" * 63).valid is True

    def test_forbidden_characters(self):
        for char in '/\\:*?"<>|':
            result = validate_mesh_name(f"mesh{char}name")
            assert not result, f"Expected failure for char: {char!r}"

    def test_name_with_spaces(self):
        # Spaces should be allowed in mesh names (common in Blender workflows)
        assert validate_mesh_name("My Mesh Object").valid is True


class TestValidateVertexCount:
    def test_valid_count(self):
        assert validate_vertex_count(100).valid is True

    def test_too_few_vertices(self):
        result = validate_vertex_count(2)
        assert not result
        assert "3" in result.error

    def test_exactly_three_vertices(self):
        assert validate_vertex_count(3).valid is True

    def test_exceeds_maximum(self):
        result = validate_vertex_count(1_000_001)
        assert not result

    def test_near_maximum_triggers_warning(self):
        result = validate_vertex_count(900_000)
        assert result.valid is True
        assert result.warning is not None

    def test_custom_max_vertices(self):
        result = validate_vertex_count(500, max_vertices=400)
        assert not result

    def test_zero_vertices(self):
        # Zero vertices should fail just like 1 or 2
        result = validate_vertex_count(0)
        assert not result
        assert "3" in result.error


class TestValidateLocation:
    def test_valid_origin(self):
        assert validate_location((0, 0, 0)).valid is True

    def test_valid_floats(self):
        assert validate_location((1.5, -3.0, 100.0)).valid is True

    def test_wrong_length(self):
        assert not validate_location((1, 2))
        assert not validate_location((1, 2, 3, 4))

    def test_non_numeric_component(self):
        result = validate_location((1, "two", 3))
        assert not result

    def test_large_value_warning(self):
        result = validate_location((2e6, 0, 0))
        assert result.valid is True
        assert result.warning is not None

    def test_negative_coordinates(self):
        # Negative coordinates are perfectly valid in Blender
        assert validate_location((-50.0, -100.0, -25.5)).valid is True


class TestValidateScale:
    def test_valid_uniform_scale(self):
        assert validate_scale((1, 1, 1)).valid is True

    def test_zero_scale_component(self):
        result = validate_scale((1, 0, 1))
        assert not result
        assert "zero" in result.error.lower()

    def test_negative_scale_allowed(self):
        assert validate_scale((-1, 1, 1)).valid is True

    def test_wrong_length(self):
        assert not validate_scale((1, 2))
