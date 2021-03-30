## Scene Graph  
### Spatial Relation based Scene Graph  
Positional relation between document components are normally represented as positional encodding which can represent the sequentially positional relationships between document components. For DLA tasks, the document components not only have sequential positional relations(followling the reading order), they also have some spatial relationships between different components. Every component will have different relatively spatial relationships between other components in same page. The initial version of spatial relationships are divided into four types including 'above', 'under', 'left', 'right' determined by calculating thier largest different bounding box coordinates.  
Nodes in this scene graph are document components and edges are the relatively spatial relationship between two nodes (components), see left section of below figure.  
![image](https://github.com/yihaoding/Document_Layout_Analysis/blob/main/Images/Scene_Graph.PNG)
### Structural Relation based Scene Graph  
Another type of scene graph is designed to represent the document structural relationships between components. The right side of above figure represents the document structural relationship between header, question and answer in a questionnaire (Funsd dataset). Nodes in this kind of scene graph also is the document components, while the edges are used to represent the structural relationships between components. This kind of scene graph can determine the structural neighbour of a component. It also can be used to emphasize some solid rules for specific domian docuemnts, for example in a scientific paper, a figure or table  must have a caption. The name of edges can be determined as the label of target components or given another appropriate name according to application scenarios.
#### Publaynet  
The document components in publaynet dataset are divided into 5 categories including title, text, list, figure and table. The possible relations between documents including *title -> title (edge: subtitle), title -> title (edge: parent title), title -> text (edge: section content), text -> title (edge: section title), title -> figure (edge: figure), table -> text (table caption) etc.* 
#### Docbank  
Docbank dataset contains 13 number of categories, but it is similar to publaynet dataset which also uses the structural relationships to annotate the type of edges in scene graph.
#### Funsd

