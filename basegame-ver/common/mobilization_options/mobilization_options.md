﻿All triggers and script evals have the following scope types:

	root = country
	scope:military_formation = military formation

specifies the type of formation this option is valid for, default army
currently only armies are valid targets for mobilization options and this option should be omitted

	military_formation_type = army

specifies which of the mobilization_option_groups this option belongs to

	group = supplies

link to a graphical representation of the mobilization option

	texture = "gfx/interface/icons/production_method_icons/unused/powered_machine_guns.dds"

keys to technologies, at least one of which is required to use

	unlocking_technologies = {
		automatic_machine_guns
	}

keys to laws, at least one of which is required to use
in this fictional example, you can only have machinegunners if you have National Guard or Secret Police

	unlocking_laws = {
		law_national_guard
		law_secret_police
	}

trigger that determines if the option can be turned off or not
in this fictional example, if you have automatic machine guns you can never not use them

	is_shown = {
		has_technology = handcranked_machine_guns
	}

trigger that determines if the option can be used or not
in this fictional example, you can only have machinegunners if you have 10 units or more in the formation

	possible = {
		scope:military_formation = {
			num_units >= 10
		}
	}

trigger that determines if the option can be turned off or not
in this fictional example, if you have automatic machine guns and more than 10 units in the formation you can never not
use them

	can_be_turned_off = {
		custom_tooltip = {
			text = mobilization_option_machinegunners_can_be_turned_off_tt
			NOT = { has_technology = automatic_machine_guns }
		}
	}

effects that run when the mobilization option is toggled accordingly

	on_activate = {}
	on_deactivate = {}
	on_activate_while_mobilized = {}
	on_deactivate_while_mobilized = {
		custom_tooltip = {
			text = mobilization_option_it_hurts_morale_when_you_remove_supplies_while_in_combat_tt
			every_combat_unit = {
				add_morale = {
					value = morale
					multiply = -0.5
				}
			}
		}
	}

goods cost when active & mobilized

	upkeep_modifier = {
		goods_input_small_arms_add = 1
		goods_input_ammunition_add = 1
	}

effects on units when active & mobilized
unit_modifier = {
unit_offense_add = 5
unit_defense_add = 10
}

script value that multiplies the AI value calculation for a mobilization option
the base AI value that is multiplied is set by the ai_value of the unit_modifier
after multiplication, this is compared against the monetary cost to determine if AI wants to activate the mobilization
option
root = military formation

	ai_weight = {
		value = 1
	}
