from database.DB_connect import DBConnect
from model.category import Category
from model.product import Product


class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def get_all_categories():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
         FROM category"""
        cursor.execute(query)
        for row in cursor:
            category = Category(row["id"], row["category_name"])
            result.append(category)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_connessioni():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT p1.id as prodotto1, p2.id as prodotto2
FROM order_item oi1, order_item oi2, 'order' o1, 'order' o2, product p1, product p2
WHERE oi1.product_id = p1.id AND oi2.product_id = p2.id AND oi1.order_id =o1.order_id AND oi2.order_id =o2.order_id AND o1.order_date BETWEEN %s AND %s AND p1.product_id <> p2.product_id
GROUP BY p1.product_name, p2.product_name
HAVING COUNT(oi1.product_id) >= 1 AND COUNT(oi2.product_id) >= 1"""
        cursor.execute(query)
        for row in cursor:
            (row["product_name"], row["product_name"])
            result.append(row["product_name"])
        cursor.close()
        conn.close()
        return result




    def get_all_products_by_category(cat):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * 
                                FROM product
                                WHERE category_id = %s """

        cursor.execute(query, (cat.id,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    def get_edges(cat, d1, d2, id_map):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT t1.id AS n1, t2.id AS n2, t1.num+t2.num AS peso
                        FROM (SELECT p.id , count(*) AS num
                              FROM product p, order_item oi, `order` o 
                              WHERE p.id = oi.product_id AND oi.order_id = o.id 
                                    AND o.order_date BETWEEN %s AND %s
                                    AND p.category_id = %s
                                    GROUP BY (p.id)
                                    ORDER BY p.id ) t1, 
                             (SELECT p.id , count(*) AS num
                              FROM product p, order_item oi, `order` o 
                              WHERE p.id = oi.product_id AND oi.order_id = o.id 
                                    AND o.order_date BETWEEN %s AND %s
                                    AND p.category_id = %s
                              GROUP BY (p.id)
                              ORDER BY p.id ) t2
                       WHERE t1.num >= t2.num
                             AND t1.id <> t2.id
                       ORDER BY peso DESC, n1 ASC, n2 ASC """

        cursor.execute(query, (d1, d2, cat.id, d1, d2, cat.id))

        for row in cursor:
            results.append((id_map[row["n1"]], id_map[row["n2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results






