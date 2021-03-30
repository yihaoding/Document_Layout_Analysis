## Scene Graph  
### Spatial Relation based Scene Graph  
Positional relation between document components are normally represented as positional encodding which can represent the sequentially positional relationships between document components. For DLA tasks, the document components not only have sequential positional relations(followling the reading order), they also have some spatial relationships between different components. Every component will have different relatively spatial relationships between other components in same page. The initial version of spatial relationships are divided into four types including 'above', 'under', 'left', 'right' determined by calculating thier largest different bounding box coordinates.  
Nodes in this scene graph are document components and relations are the relatively spatial relationship between two nodes (components).  
![image]https://github.com/yihaoding/Document_Layout_Analysis/blob/main/Images/Scene%20Graph%20Example.PNG
### Structural Relation based Scene Graph  

#### Publaynet  
#### Docbank  
#### Funsd

