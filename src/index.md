---
sql:
    enrollment_data: ./data/enrollment.parquet
    description_data: ./data/catalog_html.parquet
    annotated_data: ./data/llm.parquet
---

# Uvm Course data from enrollment
## https://www.uvm.edu/~rgweb/zoo/archive/catalogue/index.html


```sql id=count_year_enrollment
SELECT COUNT(DISTINCT (cn, title)) AS n_courses, year
FROM enrollment_data
GROUP BY year
ORDER BY year;
```

```sql id=count_year_html
SELECT COUNT(title) as n_courses, year 
FROM description_data 
GROUP BY YEAR 
ORDER BY year;
```

```sql id=count_year_annot
SELECT COUNT(DISTINCT (Number, Title)) as n_courses, year 
FROM annotated_data 
GROUP BY YEAR 
ORDER BY year;
```


```js
resize((width) => Plot.plot({
    width,
    y: {grid: true},
    color: {
        range: ["darkred", "midnightblue", "green"], 
        domain: ["count from html", "enrollment", "llm"], 
        legend: true
    },
    marginLeft: 80,
    marks: [ 
        Plot.lineY(count_year_enrollment, {x: "year", y: "n_courses", stroke: "midnightblue"}),
        Plot.dotY(count_year_html, {x: "year", y: "n_courses", stroke: "darkred"}),
        Plot.barY(count_year_annot, {x: "year", y: "n_courses", fill: "green", opacity: 0.5})
        ]
}))
```


---

# Appendix

Raw tables of the different data sources

### Course description from html table

We scraped a few years from the UVM html catalog.

```sql
SELECT title, description, year 
FROM description_data
WHERE year = '2014' 
ORDER BY title
```

### Annotated data table

```sql
SELECT * 
FROM annotated_data 
WHERE year = '2003' AND Department IN ('BIOL', 'Biology')
ORDER BY page_number, col_number
```

### Enrollment data table


Raw UVM enrollment data from the 1990s.

```sql
SELECT  dept, cn, title, COUNT(DISTINCT(dept, cn, title)) as n FROM enrollment_data WHERE year = '2003' GROUP BY dept, cn, title ORDER BY dept, cn
```

