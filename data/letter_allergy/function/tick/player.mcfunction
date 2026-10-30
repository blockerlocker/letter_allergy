execute as @a unless entity @e[type=#letter_allergy:all,distance=..5] unless entity @e[type=#letter_allergy:entity_with_contents,predicate=letter_allergy:allergy_item,distance=..5] unless items entity @s letter_allergy:whole_inventory #letter_allergy:all positioned ~-5.5 ~-5.5 ~-5.5 unless predicate letter_allergy:11x11x11 run return run execute as @s[tag=letter_allergy] run function letter_allergy:clear_actionbar

execute if predicate {type:"entity_properties",entity:"this",predicate:{periodic_tick:30}} run function letter_allergy:damage

tag @s add letter_allergy

function letter_allergy:notify