Improve markdown2html.py by parsing paragraph syntax for generating HTML:

Syntax: (you can assume it will be strictly this syntax)

Markdown:

Hello

I'm a text
with 2 lines
HTML generated:

<p>
    Hello
</p>
<p>
    I'm a text
        <br />
    with 2 lines
</p>
guillaume@vagrant:~/$ cat README.md
# My title
- Hello
- Bye

Hello

I'm a text
with 2 lines

guillaume@vagrant:~/$ ./markdown2html.py README.md README.html 
guillaume@vagrant:~/$ cat README.html 
<h1>My title</h1>
<ul>
<li>Hello</li>
<li>Bye</li>
</ul>
<p>
Hello
</p>
<p>
I'm a text
<br/>
with 2 lines
</p>
guillaume@vagrant:~/$ 
Spacing and new lines between HTML tags don’t need to be exactly this one

Repo:

GitHub repository: holbertonschool-Markdown2HTML
File: markdown2html.py
