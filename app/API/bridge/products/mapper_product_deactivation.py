def product_update(id, active, price, name, reference, slug, category_id):
    slug = slug.lower().replace(" ", "-").replace(".", "-").replace("_", "-").replace("/", "-")
    xml = f"""
    <prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
      <product>
        <id>{id}</id>
        <active>{active}</active>
        <reference><![CDATA[{reference}]]></reference>
        <state>1</state>
        <id_category_default>{category_id}</id_category_default>
        <price><![CDATA[{price}]]></price>
        <name>
          <language id="1"><![CDATA[{name}]]></language>
        </name>
        <link_rewrite>
          <language id="1"><![CDATA[{slug}]]></language>
        </link_rewrite>
      </product>
    </prestashop>"""
    return xml