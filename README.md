# <u> HBML </u>
Hyper Text Markup Language - but with braces.

[Still a work in progress]

Use similar to HTML, but instead of using `< >` all the time, we use `{ }`.

For example, a `p` tag, which would be `<p> </p>`, is now:
```
p {

}
```

When you want to have text inside this `p` tag, you use quotation marks:
```
p {
    "Text inside the paragraph!"
}
```

Alternatively, if there is only one line inside of the braces, we can use single line tags:
```
p -> "Single lined tag!"
```

When you want to specify attributes, such as `class` or `href`, we use square braces:
```
p [class="paragraph"] {
    "Text inside the paragraph!"
    
    a [href="https://github.com/Wolfsurge/HTMLBrackets"] {
        "Anchor text!"
    }
}
```

Now, this would display the anchor next to the paragraph, without any spacing. So, lets use a `br` tag
to separate them:
```
p [class="paragraph"] {
    "Text inside the paragraph!"
    
    br
    
    a [href="https://github.com/Wolfsurge/HTMLBrackets"] {
        "Anchor text!"
    }
}
```

It also works with inline elements:
```
link [rel="stylesheet", href="style.css"]
```

Comments can be declared with the '~' symbol:
```
~ This is a comment!
```

So, all together, it would look like this, as `html`, `head`, and `body` tags also exist:
```
html {
    head {
        link [rel="stylesheet", href="style.css"]
        ~ This is a comment!
    }
    
    body {
        p [class="paragraph"] {
            "Text inside the paragraph!"
            
            br
            
            a [href="https://github.com/Wolfsurge/HTMLBrackets"] {
                "Anchor text!"
            }
        }
        
        p -> "Single lined tag!"
    }
}
```

Then, when you want to turn it into HTML, execute the `main.py` script, and enter the file's path, <br>
and the HTML output will be written to a file of the same name, but with a `.html` extension!