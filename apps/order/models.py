from django.db import models
from db.base_model import BaseModel


# Create your models here.


class OrderInfo(BaseModel):
    """
    订单模型
    """

    PAY_METHODS = {
        '1': "货到付款",
        '2': "微信支付",
        '3': "支付宝",
        '4': '银联支付'
    }

    PAY_METHODS_ENUM = {
        "CASH": 1,
        "ALIPAY": 2
    }

    ORDER_STATUS_ENUM = {
        "UNPAID": 1,
        "UNSEND": 2,
        "UNRECEIVED": 3,
        "UNCOMMENT": 4,
        "FINISHED": 5
    }

    PAY_METHOD_CHOICES = (
        (1, '货到付款'),
        (2, '微信支付'),
        (3, '支付宝'),
        (4, '银联支付')
    )

    ORDER_STATUS = {
        1:'待支付',
        2:'待发货',
        3:'待收货',
        4:'待评价',
        5:'已完成'
    }

    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成')
    )
    order_id = models.CharField(max_length=128, primary_key=True, verbose_name='订单id')
    user = models.ForeignKey('user.User', verbose_name='用户', on_delete=models.CASCADE)
    addr = models.ForeignKey('user.Address', verbose_name='address', on_delete=models.CASCADE)
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=3, verbose_name='pay_method')
    total_count = models.IntegerField(default=1, verbose_name='商品数量')
    total_price = models.DecimalField(verbose_name='商品总价', max_digits=10, decimal_places=2)
    transit_price = models.DecimalField(verbose_name='运费', max_digits=10, decimal_places=2)
    order_status = models.SmallIntegerField(verbose_name='订单状态', choices=ORDER_STATUS_CHOICES, default=1)
    trade_no = models.CharField(verbose_name='支付编号', max_length=128)

    class Meta:
        db_table = 'lj_order_info'
        verbose_name = '订单'
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):
    """
    订单商品模型类
    """
    order = models.ForeignKey('OrderInfo', verbose_name='订单', on_delete=models.CASCADE)
    sku = models.ForeignKey('goods.GoodsSKU',verbose_name='商品SKU',on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='商品数目', default=1)
    price = models.DecimalField(verbose_name='商品价格', max_digits=10, decimal_places=2)
    comment = models.CharField(verbose_name='评论', max_length=256)

    class Meta:
        db_table = 'lj_order_goods'
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name
