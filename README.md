#Creating Context Free Grammars Using a Genetic Algorithm

## Getting Started

All that's needed to run is python. The source code is under the folder "real\_src/" 

### Prerequisites

Must have python 2.7

## Running the code

An example run of the code is as follows

``` 
cd real_src
python main.py
``` 

Another option to run the project is by specifying which grammars to use, as well as if you would like to test a saved population on those grammars.  

``` 
python main.py [positive_grammar_here.txt] [negative_grammar_here.txt] [starting_population.json] 
```

where positive_grammar_here.txt holds the target grammar, and negative_grammar_here are examples that do not fit the grammar. starting_population.json is for use only if you have previously saved a previous generation of rulesets and want to run it again. 

By default, the program will use a random initial population. And it will default to using "../text_files/pal.txt" as the positive grammar and "../text_files/ungram_pal.txt" as the negative one. 

## Acknowledgements

We recieved inspiration from multiple academic papers on the topic of genertic algorithms and context-free grammars.

For the implementation of the CYKParser, we used the following one: https://github.com/RobMcH/CYK-Parser. Licensing and crediting explained in "real_src/CYKParser/LICENSE.MD"

