"""In-memory product catalog and query helpers."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Category = Literal["Camping", "Hiking", "Climbing", "Water Sports", "Apparel"]
SortField = Literal["name", "price", "rating", "category"]
SortOrder = Literal["asc", "desc"]


class Product(BaseModel):
    """Catalog product returned by list endpoints."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    category: Category
    price: float
    rating: float
    stock: int
    pack_size: int = Field(serialization_alias="packSize")
    description: str


class ProductDetail(Product):
    """Product detail including computed unit pricing."""

    unit_price: float = Field(serialization_alias="unitPrice")


class ProductPage(BaseModel):
    """Paged product response."""

    items: list[Product]
    total: int
    page: int
    page_size: int = Field(serialization_alias="pageSize")


PRODUCTS: tuple[Product, ...] = (
    Product(id="camp-aurora-2p", name="Aurora Ridge 2P Tent", category="Camping", price=249.99, rating=4.8, stock=18, pack_size=1, description="Lightweight three-season tent with color-coded poles and a wide vestibule."),
    Product(id="camp-trailnest-bag", name="TrailNest 20 Sleeping Bag", category="Camping", price=139.5, rating=4.6, stock=26, pack_size=1, description="Compressible mummy bag rated to 20°F with recycled synthetic insulation."),
    Product(id="camp-summit-stove", name="SummitSpark Camp Stove", category="Camping", price=84.99, rating=4.7, stock=32, pack_size=1, description="Compact canister stove with piezo ignition and simmer control."),
    Product(id="camp-lumen-lantern", name="LumenLoop Lantern Duo", category="Camping", price=58.0, rating=4.5, stock=41, pack_size=2, description="Two rechargeable lanterns with warm dimming and magnetic bases."),
    Product(id="camp-bear-keg", name="BearVault Food Keg", category="Camping", price=96.25, rating=4.4, stock=14, pack_size=1, description="Hard-sided bear-resistant food container for multi-day trips."),
    Product(id="hike-terra-pack", name="TerraFlow 35 Pack", category="Hiking", price=169.0, rating=4.7, stock=22, pack_size=1, description="Ventilated daypack with rain cover, trekking pole keepers, and hydration sleeve."),
    Product(id="hike-granite-poles", name="GraniteLock Trekking Poles", category="Hiking", price=79.95, rating=4.6, stock=37, pack_size=2, description="Adjustable aluminum trekking poles with cork grips and carbide tips."),
    Product(id="hike-ridge-map", name="RidgeLine Map Case", category="Hiking", price=24.5, rating=4.3, stock=64, pack_size=1, description="Weatherproof fold-flat map case with lanyard and touchscreen window."),
    Product(id="hike-purify-kit", name="ClearSpring Filter Kit", category="Hiking", price=52.75, rating=4.8, stock=29, pack_size=1, description="Squeeze water filter kit rated for backcountry streams and alpine lakes."),
    Product(id="hike-first-aid", name="TrailReady First Aid Kit", category="Hiking", price=32.0, rating=4.5, stock=53, pack_size=1, description="Compact first-aid kit with blister care, wraps, and emergency instructions."),
    Product(id="climb-cragdraw-6", name="CragDraw Quickdraw Set", category="Climbing", price=109.99, rating=4.8, stock=20, pack_size=0, description="Six wiregate quickdraws for sport routes and gym lead practice."),
    Product(id="climb-chalk-cloud", name="CloudGrip Chalk Bag", category="Climbing", price=31.5, rating=4.6, stock=48, pack_size=0, description="Structured chalk bag with fleece lining, brush loop, and refillable belt."),
    Product(id="climb-belay-pro", name="BelayPro Assist Device", category="Climbing", price=119.0, rating=4.7, stock=16, pack_size=0, description="Assisted-braking belay device for single ropes and controlled lowering."),
    Product(id="climb-rope-zenith", name="Zenith 9.8 Dynamic Rope", category="Climbing", price=214.0, rating=4.9, stock=11, pack_size=0, description="Sixty-meter dry-treated rope with middle marker and supple handling."),
    Product(id="climb-harness-axis", name="Axis Comfort Harness", category="Climbing", price=89.95, rating=4.5, stock=25, pack_size=0, description="Adjustable harness with breathable waist belt and four gear loops."),
    Product(id="water-ripple-kayak", name="RippleRun Inflatable Kayak", category="Water Sports", price=399.0, rating=4.6, stock=9, pack_size=1, description="Stable one-person inflatable kayak with pump, paddle, and repair kit."),
    Product(id="water-paddle-carbon", name="CarbonWave Paddle", category="Water Sports", price=149.99, rating=4.7, stock=18, pack_size=1, description="Two-piece carbon-blend paddle with indexed ferrule and drip rings."),
    Product(id="water-drybag-trio", name="StormSeal Dry Bag Trio", category="Water Sports", price=44.5, rating=4.5, stock=57, pack_size=3, description="Three roll-top dry bags for phone, layers, and snacks on wet outings."),
    Product(id="water-pfd-breeze", name="BreezeFit PFD", category="Water Sports", price=92.0, rating=4.8, stock=21, pack_size=1, description="Low-profile paddling life vest with mesh back and reflective trim."),
    Product(id="water-reef-shoes", name="ReefGuard Water Shoes", category="Water Sports", price=39.95, rating=4.2, stock=44, pack_size=2, description="Quick-draining water shoes with grippy soles for rocky shorelines."),
    Product(id="apparel-shell", name="NimbusPeak Rain Shell", category="Apparel", price=189.0, rating=4.7, stock=30, pack_size=1, description="Waterproof breathable shell with pit zips and helmet-compatible hood."),
    Product(id="apparel-merino", name="MerinoTrail Base Layer", category="Apparel", price=74.0, rating=4.8, stock=46, pack_size=1, description="Soft merino-blend long sleeve that regulates temperature on big days."),
    Product(id="apparel-socks-3", name="SummitStride Socks", category="Apparel", price=36.0, rating=4.6, stock=73, pack_size=3, description="Three-pack of cushioned wool hiking socks with reinforced heel and toe."),
    Product(id="apparel-sun-hat", name="DesertShade Sun Hat", category="Apparel", price=42.5, rating=4.4, stock=35, pack_size=1, description="Wide-brim UPF hat with cinch cord and floating foam brim."),
)

CATEGORIES: tuple[Category, ...] = ("Camping", "Hiking", "Climbing", "Water Sports", "Apparel")


def list_categories() -> list[str]:
    """Return the supported catalog categories in display order."""
    return list(CATEGORIES)


def get_product(product_id: str) -> Product | None:
    """Find one product by id."""
    return next((product for product in PRODUCTS if product.id == product_id), None)


def query_products(
    *,
    search: str | None,
    category: str | None,
    sort: SortField,
    order: SortOrder,
    page: int,
    page_size: int,
) -> ProductPage:
    """Search, filter, sort, and page products server-side."""
    products = list(PRODUCTS)
    if category:
        products = [product for product in products if product.category == category]
    if search:
        needle = search.casefold().strip()
        products = [
            product
            for product in products
            if needle in product.name.casefold()
            or needle in product.description.casefold()
            or needle in product.category.casefold()
        ]

    def sort_value(product: Product) -> str | float:
        value = getattr(product, sort)
        return value.casefold() if isinstance(value, str) else value

    products.sort(key=sort_value, reverse=order == "desc")
    total = len(products)
    start = (page - 1) * page_size
    return ProductPage(items=products[start : start + page_size], total=total, page=page, page_size=page_size)


def build_detail(product: Product) -> ProductDetail:
    """Build product detail including computed unit price."""
    unit_price = round(product.price / product.pack_size, 2) if product.pack_size > 0 else product.price
    return ProductDetail(**product.model_dump(), unit_price=unit_price)
