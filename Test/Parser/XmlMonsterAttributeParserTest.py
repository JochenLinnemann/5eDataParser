import unittest
import Definitions
import os
import xml.etree.ElementTree as etree
from Parser.XmlMonsterAttributeParser import XmlMonsterAttributeParser as AttributeParser
from Objects.MonsterFieldsXml import MonsterFieldsXml as XML_FIELDS

unittest.TestCase.maxDiff = None


class XmlMonsterAttributeParserTest(unittest.TestCase):

    def setUp(self):
        self.monster_entry = os.path.join(Definitions.XML_RESOURCES_PATH, "Aboleth.xml")
        tree = etree.parse(self.monster_entry)
        self.root = tree.getroot().find(XML_FIELDS.MONSTER_TAG)
        self.parser = AttributeParser(self.root)

        self.monster_missing_fields = os.path.join(Definitions.XML_RESOURCES_PATH, "MissingFields.xml")
        tree = etree.parse(self.monster_missing_fields)
        self.root_missing_fields = tree.getroot().find(XML_FIELDS.MONSTER_TAG)
        self.parser_missing_fields = AttributeParser(self.root_missing_fields)

        self.custom_monster_entry = os.path.join(Definitions.XML_RESOURCES_PATH, "AbolethWithLegendaryDescription.xml")
        tree = etree.parse(self.custom_monster_entry)
        self.root = tree.getroot().find(XML_FIELDS.MONSTER_TAG)
        self.custom_parser = AttributeParser(self.root)

    def test_get_attribute_from_entry(self):

        result = self.parser.get_attribute_from_entry(self.root, XML_FIELDS.NAME)
        self.assertEquals(len(result), 1)

        result = self.parser.get_attribute_from_entry(self.root, "invalid")
        self.assertEquals(len(result), 0)

    def test_get_name(self):
        expected = "Aboleth"
        result = self.parser.get_name()
        self.assertEquals(result, expected)

        expected = ""
        result = self.parser_missing_fields.get_name()
        self.assertEquals(result, expected)

    def test_get_type(self):
        expected = "aberration"
        result = self.parser.get_type()
        self.assertEquals(result, expected)

        expected = ""
        result = self.parser_missing_fields.get_type()
        self.assertEquals(result, expected)

    def test_get_subtype(self):
        expected = "fish, mogel"
        result = self.parser.get_subtype()
        self.assertEquals(result, expected)

    def test_get_size(self):
        expected = "large"
        result = self.parser.get_size()
        self.assertEquals(result, expected)

        expected = ""
        result = self.parser_missing_fields.get_size()
        self.assertEquals(result, expected)

    def test_get_hit_points_with_dice(self):
        expected = "135 (18d10+36)"
        result = self.parser.get_hit_points_with_hit_dice()
        self.assertEquals(result, expected)

    def test_get_challenge_rating(self):
        expected = "10"
        result = self.parser.get_challenge_rating()
        self.assertEquals(result, expected)

    def test_get_languages(self):
        expected = "Deep Speech, telepathy 120 ft."
        result = self.parser.get_languages()
        self.assertEquals(result, expected)

    def test_get_senses(self):
        expected = "darkvision 120 ft."
        result = self.parser.get_senses()
        self.assertEquals(result, expected)

        expected = ""
        result = self.parser_missing_fields.get_senses()
        self.assertEquals(result, expected)

    def test_get_skills(self):
        expected = "History +12, Perception +10"
        result = self.parser.get_skills()
        self.assertEquals(result, expected)

    def test_get_saving_throws(self):
        expected = "Con +6, Int +8, Wis +6"
        result = self.parser.get_saving_throws()
        self.assertEquals(result, expected)

    def test_get_stat_scores(self):
        expected = 21
        result = self.parser.get_strength()
        self.assertEquals(result, expected)

        expected = 15
        result = self.parser.get_wisdom()
        self.assertEquals(result, expected)

        expected = 9
        result = self.parser.get_dexterity()
        self.assertEquals(result, expected)

        expected = 18
        result = self.parser.get_charisma()
        self.assertEquals(result, expected)

        expected = 18
        result = self.parser.get_intelligence()
        self.assertEquals(result, expected)

        expected = 15
        result = self.parser.get_constitution()
        self.assertEquals(result, expected)

    def test_get_speed_with_description(self):
        expected = "10 ft., swim 40 ft."
        result = self.parser.get_speed_with_description()
        self.assertEquals(result, expected)

    def test_get_armor_class_with_description(self):
        expected = "17 (natural armor)"
        result = self.parser.get_armor_class_with_description()
        self.assertEquals(result, expected)

    def test_get_alignment(self):
        expected = "lawful evil"
        result = self.parser.get_alignment()
        self.assertEquals(result, expected)

    def test_get_damage_vulnerabilities(self):
        expected = "fire"
        result = self.parser.get_damage_vulnerabilities()
        self.assertEquals(result, expected)

    def test_get_damage_resistances(self):
        expected = "acid, cold, fire, lightning, thunder, bludgeoning, piercing, and slashing from " + \
                   "nonmagical weapons that aren't silvered"
        result = self.parser.get_damage_resistances()
        self.assertEquals(result, expected)

    def test_get_damage_immunities(self):
        expected = "necrotic, poison"
        result = self.parser.get_damage_immunities()
        self.assertEquals(result, expected)

    def test_get_condition_immunities(self):
        expected = "charmed, grappled, paralyzed, petrified, poisoned, prone, restrained"
        result = self.parser.get_condition_immunities()
        self.assertEquals(result, expected)

    def test_get_special_abilities(self):
        special_ability_list = self.parser.get_special_abilities()
        self.assertNotEquals(len(special_ability_list), 0)
        ability_1 = special_ability_list[0]
        ability_2 = special_ability_list[1]
        self.assertEquals(ability_1.name, "Amphibious")
        self.assertEquals(ability_1.description, "The aboleth can breathe air and water.")
        self.assertEquals(ability_2.name, "Mucous Cloud")
        missing_special_abilities = self.parser_missing_fields.get_special_abilities()
        self.assertEquals(len(missing_special_abilities), 0)

    def test_get_attack_bonus_from_attack_string(self):
        attack_string_normal = "Tail|9|3d6+5"
        expected_normal = 9
        attack_string_weird = "Tail||3d6"
        expected_weird = 0
        attack_string_empty = ""
        expected_empty = 0
        self.assertEquals(self.parser.get_attack_bonus_from_attack_string(attack_string_empty), expected_empty)
        self.assertEquals(self.parser.get_attack_bonus_from_attack_string(attack_string_weird), expected_weird)
        self.assertEquals(self.parser.get_attack_bonus_from_attack_string(attack_string_normal), expected_normal)

    def test_get_damage_bonus_from_attack_string(self):
        attack_string_normal = "Tail|9|3d6+5"
        expected_normal = 5
        attack_string_no_bonus = "Tail|9|3d6"
        expected_no_bonus = 0
        attack_string_weird = "Tail||"
        expected_weird = 0
        attack_string_empty = ""
        expected_empty = 0
        self.assertEquals(self.parser.get_damage_bonus_from_attack_string(attack_string_empty), expected_empty)
        self.assertEquals(self.parser.get_damage_bonus_from_attack_string(attack_string_weird), expected_weird)
        self.assertEquals(self.parser.get_damage_bonus_from_attack_string(attack_string_normal), expected_normal)
        self.assertEquals(self.parser.get_damage_bonus_from_attack_string(attack_string_no_bonus), expected_no_bonus)

    def test_get_damage_dice_from_attack_string(self):
        attack_string_normal = "Tail|9|3d6+5"
        expected_normal = "3d6"
        attack_string_no_bonus = "Tail|9|3d6"
        expected_no_bonus = "3d6"
        attack_string_weird = "Tail||"
        expected_weird = ""
        attack_string_empty = ""
        expected_empty = ""
        self.assertEquals(self.parser.get_damage_dice_from_attack_string(attack_string_empty), expected_empty)
        self.assertEquals(self.parser.get_damage_dice_from_attack_string(attack_string_weird), expected_weird)
        self.assertEquals(self.parser.get_damage_dice_from_attack_string(attack_string_normal), expected_normal)
        self.assertEquals(self.parser.get_damage_dice_from_attack_string(attack_string_no_bonus), expected_no_bonus)

    def test_get_actions(self):
        actions = self.parser.get_actions()
        self.assertNotEquals(len(actions), 0)

        action_1 = actions[0]
        action_2 = actions[1]
        action_4 = actions[3]

        self.assertEquals(action_1.name, "Multiattack")
        self.assertEquals(action_1.description, "The aboleth makes three tentacle attacks.")
        self.assertEquals(action_1.damage_dice, "")
        self.assertEquals(action_1.attack_bonus, 0)
        self.assertEquals(action_1.damage_bonus, 0)

        self.assertEquals(action_2.name, "Tentacle")
        self.assertEquals(action_2.attack_bonus, 9)
        self.assertEquals(action_2.damage_bonus, 5)
        self.assertEquals(action_2.damage_dice, "2d6")

        self.assertEquals(action_4.name, "Enslave (3/day)")
        self.assertEquals(action_4.description, "The aboleth targets one creature it can see within 30 ft. of it. "
                                                "The target must succeed on a DC 14 Wisdom saving throw or be magically"
                                                " charmed by the aboleth until the aboleth dies or until it is on a "
                                                "different plane of existence from the target. The charmed target is "
                                                "under the aboleth's control and can't take reactions, and the aboleth "
                                                "and the target can communicate telepathically with each other over any"
                                                " distance.\nWhenever the charmed target takes damage, the target can "
                                                "repeat the saving throw. On a success, the effect ends. No more than "
                                                "once every 24 hours, the target can also repeat the saving throw when "
                                                "it is at least 1 mile away from the aboleth.")

    def test_get_legendary_summary(self):
        legendary_summary = self.parser.get_legendary_summary()
        expected = "The aboleth can take 3 legendary actions, choosing from the options " \
                   "below. Only one legendary action option can be used at a time, and " \
                   "only at the end of another creature's turn. The aboleth regains spent " \
                   "legendary actions at the start of its turn."
        self.assertEquals(legendary_summary, expected)

        legendary_summary = self.custom_parser.get_legendary_summary()
        expected = "Custom can take 3 legendary actions, choosing from the options " \
                   "below. Only one legendary action option can be used at a time, and " \
                   "only at the end of another creature's turn. Custom regains spent " \
                   "legendary actions at the start of his turn."
        self.assertEquals(legendary_summary, expected)

    def test_get_legendary_actions(self):
        legendary_action_list = self.parser.get_legendary_actions()
        self.assertNotEquals(len(legendary_action_list), 0)

        legendary_action_1 = legendary_action_list[0]
        legendary_action_3 = legendary_action_list[2]

        self.assertEquals(legendary_action_1.name, "Detect")
        self.assertEquals(legendary_action_1.description, "The aboleth makes a Wisdom (Perception) check.")
        self.assertEquals(legendary_action_1.damage_dice, "")
        self.assertEquals(legendary_action_1.attack_bonus, 0)
        self.assertEquals(legendary_action_1.damage_bonus, 0)
        self.assertEquals(legendary_action_3.name, "Psychic Drain (Costs 2 Actions)")
        self.assertEquals(legendary_action_3.attack_bonus, 0)
        self.assertEquals(legendary_action_3.damage_bonus, 0)
        self.assertEquals(legendary_action_3.damage_dice, "3d6")

        # Make sure it skipped the fake legendary action
        legendary_action_list = self.custom_parser.get_legendary_actions()
        self.assertEquals(len(legendary_action_list), 3)
        legendary_action_1 = legendary_action_list[0]

        self.assertEquals(legendary_action_1.name, "Detect")

    def test_get_reactions(self):
        reaction_list = self.parser.get_reactions()
        self.assertNotEquals(len(reaction_list), 0)

        reaction_1 = reaction_list[0]

        self.assertEquals(reaction_1.name, "Bonded Savior")
        self.assertEquals(reaction_1.description, "When the Abolenth's ward takes damage, the Abolenth can " +
                          "transfer the damage to itself instead. The Abolenth's damage resistance and immunity " +
                          "don't apply to transferred damage.")

    def test_get_source(self):
        result = self.parser.get_source()
        expected = "monster manual"

        self.assertEquals(result, expected)
