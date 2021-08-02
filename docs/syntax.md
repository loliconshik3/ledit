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

    "classes" : {

        "base_class" : {
            "color" : "#e90000",
            
            "syntax_list" : [
                "local", "if", "then", "elseif", "endif"
            ]
        },

        "variable_class" : {
            "color" : "#a1da1f",
            
            "syntax_list" : [
                "unit", "location", "integer", "real", "group"
            ]
        }
    }
}
```
3. Done!
