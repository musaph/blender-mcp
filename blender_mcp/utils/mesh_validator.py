"""Utility module for validating Blender mesh data before MCP operations."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationResult:
    valid: bool
    error: Optional[str] = None
    warning: Optional[str] = None

    def __bool__(self) -> bool:
        return self.valid


def validate_mesh_name(name: str) -> ValidationResult:
    """Validate a mesh/object name for Blender compatibility."""
    if not name or not name.strip():
        return ValidationResult(valid=False, error="Mesh name cannot be empty.")
    if len(name) > 63:
        return ValidationResult(
            valid=False, error=f"Mesh name exceeds 63 characters (got {len(name)})."
        )
    forbidden = set('/\\:*?"<>|')
    if any(c in forbidden for c in name):
        return ValidationResult(
            valid=False,
            error=f"Mesh name contains forbidden characters: {forbidden & set(name)}",
        )
    return ValidationResult(valid=True)


# Lowered default from 1_000_000 to 500_000 — my machine struggles with larger meshes
def validate_vertex_count(count: int, max_vertices: int = 500_000) -> ValidationResult:
    """Validate that a vertex count is within acceptable bounds."""
    if count < 3:
        return ValidationResult(
            valid=False, error=f"Mesh must have at least 3 vertices (got {count})."
        )
    if count > max_vertices:
        return ValidationResult(
            valid=False,
            error=f"Vertex count {count} exceeds maximum allowed ({max_vertices}).",
            warning="Consider decimating the mesh before sending via MCP.",
        )
    if count > max_vertices * 0.8:
        return ValidationResult(
            valid=True,
            warning=f"Vertex count {count} is close to the maximum ({max_vertices}). Performance may degrade.",
        )
    return ValidationResult(valid=True)


def validate_location(location: tuple) -> ValidationResult:
    """Validate a 3D location tuple."""
    if not isinstance(location, (list, tuple)) or len(location) != 3:
        return ValidationResult(
            valid=False, error="Location must be a sequence of exactly 3 numeric values."
        )
    for i, val in enumerate(location):
        if not isinstance(val, (int, float)):
            return ValidationResult(
                valid=False, error=f"Location component [{i}] is not numeric: {val!r}."
            )
        if abs(val) > 1e6:
            return ValidationResult(
                valid=True,
                warning=f"Location component [{i}] value {val} is very large; verify units.",
            )
    return ValidationResult(valid=True)


def validate_scale(scale: tuple) -> ValidationResult:
    """Validate a 3D scale tuple."""
    if not isinstance(scale, (list, tuple)) or len(scale) != 3:
        return ValidationResult(
            valid=False, error="Scale must be a sequence of exactly 3 numeric values."
        )
    for i, val in enumerate(scale):
        if not isinstance(val, (int, float)):
            return ValidationResult(
                valid=False,
