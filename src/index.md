---
sql:
    enrollment_data: ./data/course_catalogue_raw.parquet
    description_data: ./data/course_scraper_html.parquet
    annotated_data: ./data/course_annotated.parquet
    emb_data: ./data/embeddings.parquet
    sim_mat_phi: ./data/sim_matrix_phi.parquet
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

## Embedding time 

```sql id=[...embeddings]
SELECT * FROM emb_data
```


```js
const selcol = view(
  Inputs.select(['year', 'department', 'cluster'], {label: "color"})
);
```

```js
resize((width) => Plot.plot({
    width,
    grid: true,
    height: 600,
    color: {
        legend: true, 
        type: selcol === 'year' ? "ordinal" : "linear"
    },
    marks: [ 
        Plot.dot(embeddings.filter(d=>d.cluster != -1), {
            x: "x", y: "y", 
            fill: d => selcol === 'department' ? 
                deptMap.get(d.dept) : 
                d[selcol], 
            title: d => 
                `dept: ${d.dept}\ncluster: ${d.cluster}\nyear: ${d.year})\ndescription: ${d.description}`, tip: true
            }),
        Plot.dot(embeddings.filter(d=>d.cluster == -1), {
            x: "x", y: "y", fill: "grey", opacity: 0.1
            }),
        ]
}))
```

## Philosophy similarity matrix

<!-- ```js
resize((width) => Plot.plot({
    width,
    color: {
        legend:true
        },
    padding: 0,
    marginLeft: 80,
    marginBottom: 80,
    x: {tickRotate: 75, label: null},
    y: {label: null},
    grid: true,
    color: {type: "linear", scheme: "PiYG"},
    marks: [
        Plot.cell(phi_sim, {x: "source", y: "target", fill: "similarity", inset: 0.5}),
    ]
}))
``` -->

```sql id=[...phi_sim]
SELECT * FROM sim_mat_phi
```

```js
const selidx = view(
  Inputs.select(new Set(phi_sim.map(d=>d.source)), {label: "select index"})
);
```

```js
const targetidx = view(
  Inputs.select(new Set(phi_sim.map(d=>d.source)), {label: "target index"})
);
```

```sql
SELECT * 
FROM sim_mat_phi 
WHERE source == ${selidx} 
ORDER BY similarity DESC
```


<div class="grid grid-cols-2">
<div>
Description 1: ${embeddings[selidx].description}
</div>
<div>
Description 2: ${embeddings[targetidx].description}
</div>
</div>



---

# Appendix

```js
const uniq_dept = new Set(embeddings.map(d => d.dept))
```

```js
const deptMap = new Map(Array.from(uniq_dept).map((d, i) => [d, i]));
```

Raw tables of the different data sources

### Course description from html table

We scraped a few years from the UVM html catalog.

```sql
SELECT title, year FROM description_data WHERE year = '2015' ORDER BY title
```

### Annotated data table

```sql
SELECT * FROM annotated_data WHERE year = '2015'
```

### Enrollment data table

Raw UVM enrollment data from the 1990s.

```sql
SELECT * FROM enrollment_data 
```
