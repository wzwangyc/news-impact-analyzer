"""
A-Share Market Sector Definitions

Defines all A-share market sectors with their Chinese and English names,
descriptions, and hierarchical relationships.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Sector:
    """
    Represents an A-share market sector.

    Attributes:
        code: Sector code identifier
        name_zh: Chinese name
        name_en: English name
        description_zh: Chinese description
        description_en: English description
        parent: Parent sector code (if any)
    """

    code: str
    name_zh: str
    name_en: str
    description_zh: str
    description_en: str
    parent: str | None = None

    def get_name(self, language: str = "zh") -> str:
        """Get sector name in specified language."""
        return self.name_zh if language == "zh" else self.name_en

    def get_description(self, language: str = "zh") -> str:
        """Get sector description in specified language."""
        return self.description_zh if language == "zh" else self.description_en


# A-Share Major Sectors (SW Industry Classification Level 1)
# 申万一级行业分类
SECTORS: dict[str, Sector] = {
    # Financials - 金融
    "BANK": Sector(
        code="BANK",
        name_zh="银行",
        name_en="Banks",
        description_zh="商业银行、城商行、农商行",
        description_en="Commercial banks, city commercial banks, rural commercial banks",
    ),
    "INSURANCE": Sector(
        code="INSURANCE",
        name_zh="保险",
        name_en="Insurance",
        description_zh="人寿保险、财产保险、再保险",
        description_en="Life insurance, property insurance, reinsurance",
    ),
    "SECURITIES": Sector(
        code="SECURITIES",
        name_zh="证券",
        name_en="Securities",
        description_zh="券商、投行、期货公司",
        description_en="Brokerages, investment banks, futures companies",
    ),
    # Real Estate & Construction - 房地产与建筑
    "REAL_ESTATE": Sector(
        code="REAL_ESTATE",
        name_zh="房地产",
        name_en="Real Estate",
        description_zh="房地产开发、物业管理",
        description_en="Real estate development, property management",
    ),
    "BUILDING_MATERIALS": Sector(
        code="BUILDING_MATERIALS",
        name_zh="建材",
        name_en="Building Materials",
        description_zh="水泥、玻璃、陶瓷、其他建材",
        description_en="Cement, glass, ceramics, other building materials",
    ),
    "CONSTRUCTION": Sector(
        code="CONSTRUCTION",
        name_zh="建筑",
        name_en="Construction",
        description_zh="建筑工程、装饰装修、基础设施建设",
        description_en="Construction engineering, decoration, infrastructure",
    ),
    # Materials - 原材料
    "STEEL": Sector(
        code="STEEL",
        name_zh="钢铁",
        name_en="Steel",
        description_zh="钢铁冶炼、特钢、钢材加工",
        description_en="Steel smelting, special steel, steel processing",
    ),
    "COAL": Sector(
        code="COAL",
        name_zh="煤炭",
        name_en="Coal",
        description_zh="煤炭开采、焦化、煤化工",
        description_en="Coal mining, coking, coal chemical industry",
    ),
    "PETROCHEMICALS": Sector(
        code="PETROCHEMICALS",
        name_zh="石油石化",
        name_en="Petrochemicals",
        description_zh="石油开采、炼化、化工",
        description_en="Oil exploration, refining, chemicals",
    ),
    "NONFERROUS_METALS": Sector(
        code="NONFERROUS_METALS",
        name_zh="有色金属",
        name_en="Nonferrous Metals",
        description_zh="铜、铝、黄金、稀土、锂等",
        description_en="Copper, aluminum, gold, rare earths, lithium",
    ),
    "BASIC_CHEMICALS": Sector(
        code="BASIC_CHEMICALS",
        name_zh="基础化工",
        name_en="Basic Chemicals",
        description_zh="化肥、农药、化纤、化工原料",
        description_en="Fertilizers, pesticides, chemical fibers, raw chemicals",
    ),
    # Manufacturing - 制造业
    "AUTOMOTIVE": Sector(
        code="AUTOMOTIVE",
        name_zh="汽车",
        name_en="Automotive",
        description_zh="整车制造、零部件、新能源车",
        description_en="Vehicle manufacturing, auto parts, new energy vehicles",
    ),
    "MACHINERY": Sector(
        code="MACHINERY",
        name_zh="机械",
        name_en="Machinery",
        description_zh="工程机械、机床、机器人、通用设备",
        description_en="Construction machinery, machine tools, robots, general equipment",
    ),
    "DEFENSE": Sector(
        code="DEFENSE",
        name_zh="国防军工",
        name_en="Defense & Military",
        description_zh="航空、航天、船舶、兵器装备",
        description_en="Aviation, aerospace, shipbuilding, military equipment",
    ),
    "HOME_APPLIANCES": Sector(
        code="HOME_APPLIANCES",
        name_zh="家用电器",
        name_en="Home Appliances",
        description_zh="白色家电、小家电、厨卫电器",
        description_en="White goods, small appliances, kitchen appliances",
    ),
    # Technology - 科技
    "ELECTRONICS": Sector(
        code="ELECTRONICS",
        name_zh="电子",
        name_en="Electronics",
        description_zh="半导体、消费电子、元件、PCB",
        description_en="Semiconductors, consumer electronics, components, PCB",
    ),
    "COMPUTER": Sector(
        code="COMPUTER",
        name_zh="计算机",
        name_en="Computer",
        description_zh="软件、硬件、云服务、人工智能",
        description_en="Software, hardware, cloud services, AI",
    ),
    "COMMUNICATION": Sector(
        code="COMMUNICATION",
        name_zh="通信",
        name_en="Communication",
        description_zh="运营商、设备商、光模块、5G",
        description_en="Telecom operators, equipment, optical modules, 5G",
    ),
    # Healthcare - 医药健康
    "PHARMA": Sector(
        code="PHARMA",
        name_zh="医药生物",
        name_en="Pharmaceuticals & Biotech",
        description_zh="创新药、仿制药、医疗器械、医疗服务",
        description_en="Innovative drugs, generics, medical devices, healthcare services",
    ),
    # Consumer - 消费
    "FOOD_BEVERAGE": Sector(
        code="FOOD_BEVERAGE",
        name_zh="食品饮料",
        name_en="Food & Beverage",
        description_zh="白酒、食品、乳制品、调味品",
        description_en="Baijiu, food products, dairy, condiments",
    ),
    "TEXTILES": Sector(
        code="TEXTILES",
        name_zh="纺织服装",
        name_en="Textiles & Apparel",
        description_zh="服装、家纺、纺织制造",
        description_en="Apparel, home textiles, textile manufacturing",
    ),
    "LIGHT_INDUSTRY": Sector(
        code="LIGHT_INDUSTRY",
        name_zh="轻工制造",
        name_en="Light Industry",
        description_zh="造纸、包装、家具、文具",
        description_en="Paper, packaging, furniture, stationery",
    ),
    "RETAIL": Sector(
        code="RETAIL",
        name_zh="商贸零售",
        name_en="Retail & Trade",
        description_zh="百货、超市、电商、专业零售",
        description_en="Department stores, supermarkets, e-commerce, specialty retail",
    ),
    "CONSUMER_SERVICES": Sector(
        code="CONSUMER_SERVICES",
        name_zh="社会服务",
        name_en="Consumer Services",
        description_zh="旅游、酒店、餐饮、教育",
        description_en="Tourism, hotels, restaurants, education",
    ),
    "BEAUTY_CARE": Sector(
        code="BEAUTY_CARE",
        name_zh="美容护理",
        name_en="Beauty & Personal Care",
        description_zh="化妆品、医美、个人护理",
        description_en="Cosmetics, medical aesthetics, personal care",
    ),
    # Utilities & Transportation - 公用事业与交通
    "UTILITIES": Sector(
        code="UTILITIES",
        name_zh="电力",
        name_en="Utilities",
        description_zh="火电、水电、核电、绿电",
        description_en="Thermal power, hydro, nuclear, green energy",
    ),
    "TRANSPORTATION": Sector(
        code="TRANSPORTATION",
        name_zh="交通运输",
        name_en="Transportation",
        description_zh="航空、机场、港口、物流、铁路",
        description_en="Airlines, airports, ports, logistics, railways",
    ),
    # Agriculture - 农业
    "AGRICULTURE": Sector(
        code="AGRICULTURE",
        name_zh="农林牧渔",
        name_en="Agriculture",
        description_zh="种植、养殖、饲料、农产品加工",
        description_en="Planting, breeding, feed, agricultural processing",
    ),
    # Other - 其他
    "MEDIA": Sector(
        code="MEDIA",
        name_zh="传媒",
        name_en="Media",
        description_zh="游戏、影视、广告、出版",
        description_en="Gaming, film/TV, advertising, publishing",
    ),
    "ENVIRONMENTAL": Sector(
        code="ENVIRONMENTAL",
        name_zh="环保",
        name_en="Environmental Protection",
        description_zh="污水处理、固废处理、环境监测",
        description_en="Wastewater treatment, waste management, environmental monitoring",
    ),
}


def get_sector_list() -> list[str]:
    """Get list of all sector codes."""
    return list(SECTORS.keys())


def get_sector_names(language: str = "zh") -> dict[str, str]:
    """
    Get mapping of sector codes to names.

    Args:
        language: Language code ('zh' or 'en')

    Returns:
        Dictionary mapping sector codes to names
    """
    return {code: sector.get_name(language) for code, sector in SECTORS.items()}


def get_sector_descriptions(language: str = "zh") -> dict[str, str]:
    """
    Get mapping of sector codes to descriptions.

    Args:
        language: Language code ('zh' or 'en')

    Returns:
        Dictionary mapping sector codes to descriptions
    """
    return {code: sector.get_description(language) for code, sector in SECTORS.items()}
