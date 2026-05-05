def odoo_to_prestashop(product):
    name = product["name"]
    price = product["list_price"]
    reference = product["default_code"]

    slug = name.lower().replace(" ", "-")

    xml = f"""
    <prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
      <product>

        <id_manufacturer>1</id_manufacturer>
        <id_supplier>1</id_supplier>
        <id_category_default>10</id_category_default>
        <id_shop_default>1</id_shop_default>
        <id_tax_rules_group>0</id_tax_rules_group>

 
        <active>1</active>
        <available_for_order>1</available_for_order>
        <show_price>1</show_price>
        <product_type><![CDATA[standard]]></product_type>
        <type><![CDATA[standard]]></type>
        <new>1</new>
        <state>1</state>

        <reference><![CDATA[{reference}]]></reference>
        <supplier_reference><![CDATA[{reference}]]></supplier_reference>
        <price>{price}</price>

        <name>
          <language id="1"><![CDATA[{name}]]></language>
        </name>

        <link_rewrite>
          <language id="1"><![CDATA[{slug}]]></language>
        </link_rewrite>

        <meta_title>
          <language id="1"><![CDATA[{name}]]></language>
        </meta_title>
        <meta_description>
          <language id="1"><![CDATA[Descripción para SEO]]></language>
        </meta_description>
        <meta_keywords>
          <language id="1"><![CDATA[Palabras clave]]></language>
        </meta_keywords>

        <associations>
          <categories>
            <category>
              <id>10</id>
            </category>
          </categories>
        </associations>

      </product>
    </prestashop>
    """

    return xml