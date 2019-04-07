from django.db import models

from tinymce.models import HTMLField
from db.base_model import BaseModel


# Create your models here.


class GoodsType(BaseModel):
    """
    商品类型模型类
    """
    name = models.CharField(verbose_name='GoodsTypeName', max_length=20)
    logo = models.CharField(verbose_name='标识', max_length=20)
    image = models.ImageField(verbose_name='商品类型图片', upload_to='type')

    class Meta:
        db_table = 'df_goods_type'
        verbose_name = '商品种类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsSKU(BaseModel):
    """
    商品SKU模型
    """
    status_choice = (
        (1, '上线'),
        (0, '下线')
    )
    type = models.ForeignKey('GoodsType', verbose_name='商品种类')
    goods = models.ForeignKey('Goods', verbose_name='商品SPU')
    name = models.CharField(verbose_name='商品名称', max_length=20)
    desc = models.CharField(verbose_name='商品简介', max_length=256)
    price = models.DecimalField(verbose_name='商品价格', max_digits=10, decimal_places=2)
    unite = models.CharField(verbose_name='商品单位', max_length=20)
    image = models.ImageField(verbose_name='商品图片', upload_to='goods')
    stock = models.IntegerField(verbose_name='商品库存', default=1)
    sales = models.IntegerField(verbose_name='商品销量', default=0)
    status = models.SmallIntegerField(verbose_name='商品状态', default=1, choices=status_choice)


class Goods(BaseModel):
    """
    商品SPU
    """
    name = models.CharField(verbose_name='Goods name', max_length=20)
    detial = HTMLField(verbose_name='Goods detail', blank=True)

    class Meta:
        db_table = 'df_goods'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name


class GoodsImage(BaseModel):
    """
    商品图片类
    """
    sku = models.ForeignKey('Goods', verbose_name='商品')
    image = models.ImageField(verbose_name='图片路径', upload_to='goods')

    class Meta:
        db_table = 'df_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name


class IndexGoodsBanner(BaseModel):
    """
    首页轮播图片
    """
    sku = models.ForeignKey('GoodsSKU', verbose_name='库存商品')
    image = models.ImageField(verbose_name='picture', upload_to='banner')
    index = models.SmallIntegerField(verbose_name='展示顺序', default=0)

    class Meta:
        db_table = 'df_index_banner'
        verbose_name = '首页轮播商品'
        verbose_name_plural = verbose_name


class IndexTypeGoodsBanner(BaseModel):
    """
    首页分类商品展示模型类
    """
    DISPLAY_TYPE_CHOICE = (
        (0, '标题'),
        (1, '图片')
    )

    type = models.ForeignKey('GoodsType', verbose_name='商品类型')
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品SKU')
    display_type = models.SmallIntegerField(verbose_name='展示类型', choices=DISPLAY_TYPE_CHOICE, default=0)
    index = models.SmallIntegerField(verbose_name='展示顺序', default=0)

    class Meta:
        db_table = 'df_index_type_goods'
        verbose_name = '主页分类展示商品'
        verbose_name_plural = verbose_name


class IndexPromotionBanner(BaseModel):
    """
    首页促销活动模型类
    """
    name = models.CharField(verbose_name='活动名称', max_length=20)
    url = models.URLField(verbose_name='链接地址')
    image = models.ImageField(verbose_name='活动图片', upload_to='banner')
    index = models.SmallIntegerField(verbose_name='展示顺序', default=0)

    class Meta:
        db_table = 'df_index_promotion'
        verbose_name = '主要促销活动'
        verbose_name_plural = verbose_name
