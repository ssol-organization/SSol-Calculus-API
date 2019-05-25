# Calculus API

Microsserviço construído em Flask que tem como objetivo gerar os diagramas feitos a partir da análise de estruturas da situação presente no experimento, consome a API de processamento de imagens para adquirir as informações das variaveis envolvidas na situação fisica.

## Endpoints
### ```/get_diagram```

Objetivo: Disponibilizar os diagramas referentes a um estado específico das váriaveis envolvidas no experimento. Retorna uma imagem no formato png.

#### Parâmetros: 

##### ```tipo```: utilizado para escolher qual diagrama será mostrado, de acordo com a tabela abaixo. 

| tipo | Descrição |
| :--: | :--: |
| 0| Diagrama Estrutural|
| 1| Forças de reação|
| 2| Axial|
| 3| Esforço Cortante|
| 4| Momento Fletor|
| 5| Displacement|

## Exemplo de uso

Nesse exemplo, o parâmetro do tipo foi o 0. Já a situação simulada foi a de dois apoios nas extremidades da barra, um de segundo gênero e um de primeiro, e uma carga pontual no centro, de 10N.

![exemplo](https://i.imgur.com/aiuUnEh.png)


<hr/>
<p align="center"><b>SSol</b></p>
<p align="center">Projeto Integrador de Engenharias 1<br /><br />
<a href="https://fga.unb.br" target="_blank"><img width="230"src="https://4.bp.blogspot.com/-0aa6fAFnSnA/VzICtBQgciI/AAAAAAAARn4/SxVsQPFNeE0fxkCPVgMWbhd5qIEAYCMbwCLcB/s1600/unb-gama.png"></a>
</p>
