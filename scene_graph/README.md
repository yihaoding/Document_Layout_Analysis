# Scene Graph  
## Spatial Relation based Scene Graph  
Positional relation between document components are normally represented as positional encodding which can represent the sequentially positional relationships between document components. For DLA tasks, the document components not only have sequentially positional relations(followling the reading order), they also have relatively spatial relationships between different components. Every component will have different relatively spatial relationships between other components in same page based on their location in a document page. The initial version of spatial relationships are divided into four types including 'above', 'below', 'left', 'right' determined by calculating thier largest different bounding box coordinates.  
Nodes in this scene graph are document components and edges are the relatively spatial relationship between two nodes (components), see left section of below figure.  
![image](https://github.com/yihaoding/Document_Layout_Analysis/blob/main/Images/Scene_Graph.PNG)
## Structural Relation based Scene Graph  
Another type of scene graph is designed to represent the document structural relationships between components. The right side of above figure represents the document structural relationship between header, question and answer in a questionnaire (Funsd dataset). Nodes in this kind of scene graph also is the document components, while the edges are designed to represent the structural relationships between components. The benefit of this kind of scene graph is it can determine the structural neighbour of a component as well sa it can also be used to emphasize some solid rules for specific domian docuemnts. For example in a scientific paper, a figure or table  must have a caption. The name of edges can be determined as the label of target components or given another appropriate name according to application scenarios.
### Publaynet  
The document components in publaynet dataset are divided into 5 categories including title, text, list, figure and table. The possible relations between documents including:  
***title -> title (edge: subtitle)  
title -> title (edge: parent title)  
title -> text (edge: section content)  
text -> title (edge: section title)  
title -> figure (edge: figure)  
table -> text (edge: table caption)  
text -> figure (edge: mentioned)*** 
### Docbank  
Docbank dataset contains 13 number of categories, but it is similar to publaynet dataset which also uses the structural relationships to annotate the type of edges in scene graph.
### Funsd
Funsd dataset contains 4 components categories including header, question, answer and other. The typical structural relationships include:    
***question -> answer (edge: 'answer' or 'answer of question')  
answer -> question (edge: 'question' or 'question of answer')  
question -> header (edge: 'header', 'header of question) and more.***
