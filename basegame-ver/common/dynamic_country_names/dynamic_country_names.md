﻿	TAG = {
		dynamic_country_name = {
			name = string # This can be left empty, and then default tag name will be used
			adjective = string # This can be left empty, and then default tag adjective will be used

			is_main_tag_only = yes # default no, if yes then only the primary country for a definition can use this name (ie Poland, not dynamic Silesia-Poland)
			priority = 0 # default 0, if multiple names have valid triggers, higher priority is used. If same priority, first one in file is used
		
			# Scripted trigger, country-scope
			trigger = {
			}
		}	
	}