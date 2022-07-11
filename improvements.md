# Юзаем django-mptt
## Получаем категории
`Category.objects.alias(non_empty=Count('category')).filter(non_empty__gt=0, level=0)`

Остальное не меняем

---
## Получаем *под*категории
Нужна проверка на то, что это **листья**


`children_query_set = category.get_children()`

`is_leaf_nodes = all((cat.is_leaf_node() for cat in children_query_set))`

Если это так, то у нас подкатегории ведущие к товарам

`children_query_set.alias...`

Иначе уводим вглубь

---
## Разработка алгоритма прохода в n-мерную глубину по подкатегориям

