# Calculus API

This microservice is dedicated to generate the diagrams that will be outputed to the users from the data input received from the Image Process API. It uses a virtual enviroment to execute with Flask and the python library AnaStruct to generate the output.

## Endpoints
### ```/get_diagram```

Objetivo: Disponibilizar os diagramas referentes a um estado específico das váriaveis envolvidas no experimento.

#### Parâmetros: 

##### ```tipo```: utilizado para escolher qual diagrama será mostrado, de acordo com a seguinte tabela: 

| tipo | Descrição |
| :--: | :--: |
| 0| Diagrama Estrutural|
| 1| Forças de reação|
| 2| Axial|
| 3| Esforço Cortante|
| 4| Momento Fletor|
| 5| Displacement|


<hr/>
<p align="center"><b>SSol</b></p>
<p align="center">Projeto Integrador de Engenharias 1<br /><br />
<a href="https://fga.unb.br" target="_blank"><img width="230"src="https://4.bp.blogspot.com/-0aa6fAFnSnA/VzICtBQgciI/AAAAAAAARn4/SxVsQPFNeE0fxkCPVgMWbhd5qIEAYCMbwCLcB/s1600/unb-gama.png"></a>
</p>
