#import numpy as np


def fullsupport(x: float, y: float = 3):
    """
    Take the max between two numbers

    **Parameters**

    > **x:** `float` -- Description of parameter `x`.

    > **y:** `float` -- Description of parameter `y`.

    **Returns**

    > `float` -- Description of returned object.

    #### Heading 4 <small>with secondary text</small>

    !!! note "note block"
        Add a personnal remark here

    !!! warning "warning block"
        Add details about the possible problems

    !!! success "success block"
        Something you're proud of ? Tell it here

    !!! summary "summary block"
        A summary block

    !!! question "question"
        Any question

    !!! tip "tip block"
        Any tip to share ?

    !!! bug "bug block"
        Oups!

    !!! quote "quote block"
        Oups!

    !!! fail "fail block"
        A fail block

    !!! info "info block"
        You need to add more context or more informations

    !!! error "error block"
        Sometimes things go wrong

    !!! example "example block"
        Illustrate your point with an example

    ??? note "note block with display"
        You can also add note on a block that can be hidden

    ???+ note "open by default"
        And it can be open by default

    Of course there is emoji :heart:

    and code inline with syntax highlights: `#!py3 import numpy as np`

    Link to other sites (http://www.google.com) or other part of the doc [function test](zoomext.md#test)

    "Magic Space": **&lt;sp&gt;** Hard space for destination markdown source

    "Magic Tab": **&lt;tab&gt;** Hard tab / indent for destination markdown source   

    <tab>here is an implicit "code/command/quote block" via Magic Tab
    <tab>an adjacent line magic tabbed in...

    A normal text section...

    <tab>another line magic tabbed in...    
    
    ```
    Inside a multi-line Code Block {
    <sp>Leading Magic Space 
    <tab>Leading Magic Tab 
    }
    ```        
    """
    #return np.max(x, y)
    return x


def test(x: int):
    """
    no doc
    """
    return
