    game_rule = {
        default = setting_name 						# Which setting to default to
    
        setting_name = {
            apply_modifier = category:modifier_key	# Apply a modifier to characters matching a specific category. Valid are player, ai, and all. E.G., player:very_easy
            flag = flag_key							# Has some specific effect. See "flags" section for list
        }
    }

rule_<key> will be used as the key for game rule names  
setting_<key> will be used as the key for game rule setting names  
setting_<key>_desc will be used as the key for game rule setting descs

# Flags

| Flag                            | ???                                                                                    |
|---------------------------------|----------------------------------------------------------------------------------------|
| blocks_achievements             | Achievements cannot be earned while this flag is active                                |
| lenient_ai                      | ???                                                                                    |
| harsh_ai                        | ???                                                                                    |
| low_ai_aggression               | ???                                                                                    |
| high_ai_aggression              | ???                                                                                    |
| no_subject_flags                | Subject nations' flags do not include their Overlord's flag as a canton                |
| no_subject_map_color            | Subject nations do not share their Overlord's map color                                |
| disable_<production_method_key> | The specified production method cannot be activated under any circumstances            |
| force_<production_method_key>   | The specified production method is forcibly activated and cannot be switched away from |
