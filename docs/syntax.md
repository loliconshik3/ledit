<h1 align="center">How to add syntax highlight</h1>
<h3 align="center">Realy, how???</h3>

# Instruction

1. Create `{langname}.json` file in `syntax` directory.

2. Use this code for example (You can add so many classes as you like):

```json
{
    "file_extension" : ["j"],

    "syntax_accept_chars" : [
        "", " ", "(", ")", "{", "}", "[", "]", ":", "="
    ],

    "function_syntax" : "function {name} takes",
    "function_color" : "#dcc46c",

    "classes" : {

        "base_class" : {
            "color" : "#e90000",
            "color_everywhere" : false,
            
            "syntax_list" : [
                "local", "if", "then", "elseif", "endif"
            ]
        },

        "variable_class" : {
            "color" : "#a1da1f",
            "color_everywhere" : false,
            
            "syntax_list" : [
                "unit", "location", "integer", "real", "group"
            ]
        }
    },

    "macros" : {
        "function" : "function name takes nothing returns nothing\n\tcall DoNothing()\nendfunction",
        "loop" : "loop\n\texitwhen index > num\n\tcall DoNothing()\n\tset index = index + 1\nendloop"
    }
}
```
3. Done!
