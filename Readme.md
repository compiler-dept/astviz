# Setup

    pip install astviz

# Usage

    astviz example.ast

# Input format

The input format is very simple. Here are some examples.

Create a root node **A** with two child nodes **B** and **C**:

``` (A(B)(C)) ```

Add another two child nodes **D** and **E** to **B**:

``` (A(B(D)(E))(C)) ```

Node names may contain any character obviously excluding '(' and ')'.

``` (A(B(D)(Node names may contain any character excluding parenthesis!))(C)) ```
