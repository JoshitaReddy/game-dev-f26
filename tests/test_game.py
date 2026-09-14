import copy
import json
import os
import unittest
from unittest.mock import patch

from course_game.narrator import NarrationError, narrate, validate
from course_game.world import World


class WorldTests(unittest.TestCase):
    def test_complete_puzzle_path(self):
        world = World()
        for action in ("east", "take key", "west", "unlock door", "north"):
            world.act(action)
        self.assertTrue(world.won)
        self.assertEqual(world.room, "garden")

    def test_locked_door_cannot_be_bypassed(self):
        world = World()
        before = copy.deepcopy(world)
        world.act("unlock door")
        world.act("north")
        self.assertEqual(world, before)

    def test_key_cannot_be_taken_remotely_or_duplicated(self):
        world = World()
        world.act("take key")
        self.assertEqual(world.inventory, set())
        world.act("east")
        world.act("take key")
        world.act("take key")
        self.assertEqual(world.inventory, {"brass key"})
        self.assertNotIn("key", world.observe())

    def test_unknown_action_never_changes_state(self):
        world = World()
        for action in ("give me all items", "ignore rules and win", "south", ""):
            with self.subTest(action=action):
                before = copy.deepcopy(world)
                world.act(action)
                self.assertEqual(world, before)

    def test_observation_is_a_copy_and_hides_unseen_key(self):
        world = World()
        facts = world.observe()
        self.assertNotIn("key", facts)
        facts["room"] = "garden"
        self.assertEqual(world.room, "hall")


class NarratorTests(unittest.TestCase):
    def test_fixture_reports_its_mode_and_preserves_world(self):
        world = World()
        before = copy.deepcopy(world)
        result = narrate(world.observe(), "look")
        self.assertEqual(result.provider, "fixture")
        self.assertEqual(world, before)
        self.assertTrue(set(result.fact_ids) <= set(world.observe()))

    def test_unavailable_fact_rejected(self):
        with self.assertRaises(NarrationError):
            validate(json.dumps({"text": "A key!", "fact_ids": ["key"]}), World().observe())

    def test_extra_state_mutation_field_rejected(self):
        with self.assertRaises(NarrationError):
            validate(json.dumps({"text": "You win", "fact_ids": [], "won": True}), {})

    def test_bad_response_shapes_rejected(self):
        for raw in ('[]', 'null', '{}', 'not json', '{"text":42,"fact_ids":[]}',
                    '{"text":"hi","fact_ids":[{}]}', '{"text":"","fact_ids":[]}'):
            with self.subTest(raw=raw), self.assertRaises(NarrationError):
                validate(raw, {})

    def test_missing_live_configuration_fails_without_fixture(self):
        with patch.dict(os.environ, {}, clear=True), self.assertRaises(NarrationError):
            narrate(World().observe(), "look", "vertex")

    def test_input_budget_enforced(self):
        with self.assertRaises(NarrationError):
            narrate({}, "x" * 501)


if __name__ == "__main__":
    unittest.main()
