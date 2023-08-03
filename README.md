## Beav

Write LOGO, but for controlling UAVs (and potentially AUVs) rather than controlling a boring turtle! Currently being written. Will also include utilities to potentially deal with sensor data, because that is the ultimate difference between an "unalive" turtle and an UAV/AUV in real life.

## The LOGO Programming Language

This entire excerpt is copied directly from MIT's library discussing, just to give an idea of what commands Beav should have at the minimum.

<details>
    <summary>Excerpt</summary>

The Logo Programming Language, a dialect of Lisp, was designed as a tool for learning. Its features - interactivity, modularity, extensibility, flexibility of data types - follow from this goal.

### Interactivity

Although there are some versions of Logo that compile, it is generally implemented as an interpreted language. The interactivity of this approach provides the user with immediate feedback on individual instructions, thus aiding in the debugging and learning process. Error messages are descriptive. For example

```
fowad

> I don't know how to fowad
```

(The word `fowad` is not a primitive - one of Logo's built in words - nor a procedure that you've defined.)

```
forward

> Not enough inputs to forward
```

(Now that you've spelled it correctly, Logo knows the word `forward`, but can't run your instruction because `forward` requires additional information.

```
forward 100
```

(Logo is happy. There's no error message. The turtle moves forward 100 steps.)

### Modularity and Extensibility

Logo programs are usually collections of small procedures. Generally, procedures are defined by writing them in a text editor. The special word `to` is followed by the name of the procedure. Subsequent lines form the procedure definition. The word `end` signals that you're finished.

In our [turtle graphics](https://el.media.mit.edu/logo-foundation/what_is_logo/logo_primer.html) example we defined a procedure to draw a square:

```logo
to square
    repeat 4 [
        forward 50
        right 90
    ]
end
```

and used it as as a subprocedure of another procedure

```logo
to flower
    repeat 36 [
        right 10
        square
    ]
end
```

Similarly, `flower` could be a building block of something larger.

```logo
to garden
    repeat 25 [
        set-random-position
        flower
    ]
end
```

No, `set-random-position` is not a primitive, but `random` is and so is `setposition` (or `setpos` or `setxy`). Or you could write `set-random-position` using `forward` and `right` with `random`.

Once a Logo procedure is defined it works like the Logo primitives. In fact, when you look at Logo programs there's no way of knowing which words are primitives and which are user-defined unless you know that particular Logo implementation. In our [language](https://el.media.mit.edu/logo-foundation/what_is_logo/logo_and_natural_language.html) sample we used the procedure `pick` to randomly select an item from a list, for example in the procedure who.

```logo
to who
    output pick [Sandy Dale Dana Chris]
end
```

In some versions of Logo `pick` is a primitive while in others you have to write it yourself. `who` would look and work the same way in either case.

Logo allows you to build up complex projects in small steps. Programming in Logo is done by adding to its vocabulary, teaching it new words in terms of words it already knows. In this way it's similar to the way people learn spoken language.

### Flexibility

Logo works with words and lists. A Logo word is a string of characters. A Logo list is an ordered collection of words and or lists. Numbers are words, but they're special because you can do things like arithmetic with them.

Many programming languages are pretty strict about wanting to know exactly what kind of data you claim to be using. This makes things easier for the computer, but harder for the programmer. Before adding a couple of numbers you might have to specify whether they are integers or real numbers. The computer needs to know such things. But most people don't think about this so Logo takes care of it for you. When asked to do arithmetic Logo just does it.

```logo
print 3 + 4
> 7

print 3 / 4
> .75
```

If you are unfamiliar with Logo but work in other programming languages, the following sequence may surprise you:

```logo
print word "apple "sauce
> applesauce

print word "3 "4
> 34

print 12 + word "3 "4
46
```

Here's a recursive procedure that computes factorials:

```logo
to factorial :number
    if :number = 1 [
        output 1
    ]

    output :number * factorial :number - 1
end

print factorial 3
> 6

print factorial 5
> 120
```

Here's a process to reverse a list of words:

```logo
to reverse :stuff
    ifelse equal? count :stuff 1
    [output first :stuff]
    [output sentence reverse butfirst :stuff first :stuff]
end

print reverse [apples and pears]

> pears and apples
```

</details>

## Okay, but like, what's new?

Sensors.

## Name?

Beav is short of beaver. Beaver is MIT's mascot, specifically for the [Beaver Works Summer Institute]().
