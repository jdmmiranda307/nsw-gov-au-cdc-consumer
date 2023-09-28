# nsw-gov-au-cdc-consumer
## Usando filtros
Caso queira filtrar sua request, alterar o dict "filters" na main de forma semelhante ao exemplo abaixo
```
ops =[{
            "name": "DA",
            "filters": {
                "ApplicationStatus": "Determined",
                "DeterminationDateFrom": "2018-01-01", 
                "DeterminationDateTo": datetime.now().strftime("%Y-%m-%d"), 
                "ApplicationType": "Development application"
            }
}]
```
Esse seria um exemplo de filtro aplicado a base DA.
Sinta-se livre pra alterar os headers e a URL, ou adicionar novos sufixos.