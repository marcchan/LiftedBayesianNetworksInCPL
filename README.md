# Lifted Bayesian Networks In Conditional Probability Logic
## Project Introduction:
This project is based on Paper:[Statistical Relational Artificial Intelligence with Relative Frequencies: A Contribution to Modelling and Transfer Learning across Domain Sizes](https://epub.ub.uni-muenchen.de/76444/) by Dr.Felix Weitkämper.

 Currently is mainly a typical LBN-CPL example.
### Example Description:
A very simple example in LBN-CPL is:
The likelihood of a driver being fined depends on two factors:
the air quality and the  frequency of people driving:
* For every person, the probability of he drives is 50%
* When the frequence of drives less than a half, i.e. the number of drives people is less than a half, the probability of good air is 80%;otherwise, is 60%
* If the air is good, City will hardly be fined(10%); if the air is not good and the frequency of drivers less than 70%, city will slightly be fined(30%); if the air is not good and the frequency of drivers more than 70%, city will be fined be fined Very likely (80%)

[//]: # ()
[//]: # (![]&#40;examples/drive_air_city/formulas_v2.png&#41;)

[//]: # ()
[//]: # ()
[//]: # (#### Domain:)

[//]: # (this example will be in the specify domain, for example:)

[//]: # ()
[//]: # (``Domain: {Paul, James, Alice,...}``)

[//]: # ()
[//]: # (#### GAP:)

[//]: # ()
[//]: # (![]&#40;examples/drive_air_city/GAP.png&#41;)

[//]: # ()
[//]: # (## Project requirements)

[//]: # ()
[//]: # ([Python]&#40;https://www.python.org/downloads/&#41; 3.7 is required to run this project)

[//]: # (### Suggestion: using conda env)

[//]: # (Install Anacoda on [Linux]&#40;https://docs.anaconda.com/anaconda/install/linux/&#41;\)

[//]: # (Install Anaconda on [MacOS]&#40;https://docs.anaconda.com/anaconda/install/mac-os/&#41;)

[//]: # ()
[//]: # (Create a virtual Environmet via Anaconda\)

[//]: # (`conda create -n yourenvname python=3.7 anaconda`)

[//]: # ()
[//]: # (Activate your Environment\)

[//]: # (`source activate yourenvname`)

[//]: # ()
[//]: # (Install the all needed dependencies\)

[//]: # (`pip install -r requirements.txt`)

[//]: # ()
[//]: # (##  Format Definition:)

[//]: # ( ### Domain)

[//]: # ( * use json format, has 3 attribute: name, type and domain.)

[//]: # (    * type currently has `int`, `bool`, `list`.)

[//]: # ( * For example:)

[//]: # (    ```)

[//]: # (    {)

[//]: # (      "nodes": [)

[//]: # (        {)

[//]: # (          "name": "Drives",)

[//]: # (          "type": "int",)

[//]: # (          "domain":"4")

[//]: # (        },)

[//]: # (        {)

[//]: # (          "name": "Air_is_good",)

[//]: # (          "type": "bool",)

[//]: # (          "domain": "[True, False]")

[//]: # (        },)

[//]: # (        {)

[//]: # (          "name": "Fined",)

[//]: # (          "type": "bool",)

[//]: # (          "domain": "[True, False]")

[//]: # (        })

[//]: # (      ])

[//]: # (    })

[//]: # (   ```)

[//]: # ()
[//]: # (###Formula)

[//]: # (  * `<Nodename> ::`means the following formulas is for `<Nodename>`)

[//]: # (  * Between 2 node formulas there are **`blank line`**  for separation.)

[//]: # (  * Probabilistic logic symbol map:)

[//]: # (    * **`!`**: not)

[//]: # (    * **`|| A ||`**:  the frequence of node A)

[//]: # (    * **`&`**: logical AND)

[//]: # (    * **`|`**: logical OR)

[//]: # (    * **`¬`**: logical NOT)

[//]: # (  * **Example**:)

[//]: # (      ```)

[//]: # (        Drives::)

[//]: # (        0.5)

[//]: # (        )
[//]: # (        Air_is_good::)

[//]: # (        ||Drives <= 0.5|| : 0.8)

[//]: # (        ||Drives > 0.5|| : 0.6)

[//]: # (        )
[//]: # (        Fined::)

[//]: # (        Air_is_good : 0.1)

[//]: # (        !Air_is_good & ||Drives >= 0.7|| : 0.8)

[//]: # (        !Air_is_good & ||Drives < 0.7|| : 0.3)

[//]: # (      ```)

[//]: # ()
[//]: # (        )
[//]: # (### Change Formula V_1    )

[//]: # ( * **Example**:)

[//]: # (    * **Formula**)

[//]: # (      ```)

[//]: # (        Drives:: { X : people }    )

[//]: # (        0.5)

[//]: # (        )
[//]: # (        Fined:: {})

[//]: # (        ...)

[//]: # (        )
[//]: # (        attends:: { X : student })

[//]: # (        ||attends&#40;x&#41; >= 0.95|| & ||good_grade&#40;x&#41; >= 0.30|| : 0.95)

[//]: # (        ...)

[//]: # (        )
[//]: # (        friend :: { X : name, Y : name })

[//]: # (        ...)

[//]: # (        )
[//]: # (        Teaches:: { X: Teacher, Y: student })

[//]: # (        )