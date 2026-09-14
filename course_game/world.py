"""The deterministic game is authoritative; narration cannot mutate it."""

from dataclasses import dataclass, field


@dataclass
class World:
    room: str = "hall"
    inventory: set[str] = field(default_factory=set)
    key_taken: bool = False
    door_open: bool = False
    won: bool = False

    def observe(self) -> dict[str, str]:
        facts = {
            "room": f"You are in the {self.room}.",
            "inventory": "You carry " + (", ".join(sorted(self.inventory)) or "nothing") + ".",
        }
        if self.room == "hall":
            facts["exits"] = "The workshop is east. A locked garden door is north."
            if self.door_open:
                facts["exits"] = "The workshop is east. The garden door is open to the north."
        elif self.room == "workshop":
            facts["exits"] = "The hall is west."
            if not self.key_taken:
                facts["key"] = "A brass key rests on the workbench."
        else:
            facts["ending"] = "You reached the garden. The gatekeeper welcomes you. You win."
        return facts

    def act(self, command: str) -> str:
        command = " ".join(command.lower().split())
        if command == "look":
            return " ".join(self.observe().values())
        if self.won:
            return "The game is complete. Start a new game to play again."
        if command == "east" and self.room == "hall":
            self.room = "workshop"
        elif command == "west" and self.room == "workshop":
            self.room = "hall"
        elif command == "take key" and self.room == "workshop" and not self.key_taken:
            self.key_taken = True
            self.inventory.add("brass key")
            return "You take the brass key."
        elif command == "unlock door" and self.room == "hall":
            if "brass key" not in self.inventory:
                return "You need the brass key."
            self.door_open = True
            return "You unlock the garden door."
        elif command == "north" and self.room == "hall":
            if not self.door_open:
                return "The garden door is locked."
            self.room = "garden"
            self.won = True
        else:
            return "That action is unavailable here. Try look."
        return self.act("look")
