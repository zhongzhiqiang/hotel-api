# coding:utf-8
# Time    : 2018/10/20 下午10:25
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets
from rest_framework.decorators import detail_route

from main.models import Order
from main.common.defines import OrderType, OrderStatus
from main.apps.admin_refunded import serializers, filters
from main.common.permissions import PermsRequired


refund_status = [OrderStatus.pre_refund, OrderStatus.refund_ing, OrderStatus.refunded,
                 OrderStatus.apply_refund, OrderStatus.fill_apply, OrderStatus.refunded_fail]


class HotelRefundedViews(mixins.ListModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """
    list:
        订单状态：
                ORDER_STATUS = (
        (10, '待支付'),
        (25, '待入住'),
        (30, '入住中'),
        (35, '完成待评价'),
        (40, '完成并且已评价'),
        (45, '取消'),
        (46, '申请退款'),
        (50, '待退款'),
        (55, '退款中'),
        (60, '已退款'),
        (61, '拒绝退款'),
        (65, '已过期')
        )
        返回当前所有待退款, 退款中, 退款完成, 退款失败的订单.
        WX_REFUND_STATUS = (
        (10, '退款中'),
        (20, '成功'),
        (30, '失败'),
        (40, '重试'),
        (50, '未知')
        )
        ```
        refunded_account 为退款到账时间
        ```
    partial_update:
        退款接口 与put接口二选一
    update:
        退款接口
    retrieve:
        返回详细信息
    retry:
        重新退款，大多数情况下为微信支付的。退款条件为订单的状态为退款中且退款的状态为失败或重试
    # 还差微信退款查询接口。已经重新退款接口

    """
    queryset = Order.objects.filter(order_type=OrderType.hotel,
                                    order_status__in=refund_status).order_by('-id')
    serializer_class = serializers.HotelOrderRefundedSerializer
    filter_class = filters.OrderFilter
    permission_classes = (PermsRequired('main.refunded'), )

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        if hasattr(self.request.user, 'staffprofile'):
            return self.queryset.filter(belong_hotel=self.request.user.staffprofile.belong_hotel)
        return self.request

    def perform_update(self, serializer):
        serializer.save(operator_name=self.request.user.staffprofile)

    def get_serializer_class(self):
        if self.action == 'retry':
            return serializers.HotelOrderRetryRefundedSerializer
        return self.serializer_class

    @detail_route(methods=['POST'])
    def retry(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)


class MarketRefundedViews(mixins.ListModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """
    list:
        订单状态：
                订单状态对应的数字。
         ORDER_STATUS = (
        (10, '待支付'),
        (15, '待发货'),
        (20, '待收货')
        (35, '待评价'),
        (40, '已评价'),
        (45, '取消'),
        (46, '申请退款'),
        (48, '填写退货信息'),
        (50, '待退款'),
        (55, '退款中'),
        (60, '已退款'),
        (61, '退款失败'),
        (65, '已过期')
        )
           返回当前所有待退款, 退款中, 退款完成, 退款失败的订单.
           WX_REFUND_STATUS = (
        (10, '退款中'),
        (20, '成功'),
        (30, '失败'),
        (40, '重试'),
        (50, '未知')
        )
        ```
        refunded_account 为退款到账时间
        ```
    partial_update:
        退款接口 与put接口二选一
    update:
        退款接口
    retrieve:
        返回详细信息
    retry:
        重新退款，大多数情况下为微信支付的。退款条件为订单的状态为退款中且退款的状态为失败或重试
    deal_apply:
        处理退款申请
        order_status = ['48', '61'] # 拒绝退款传递`61`。同意退款传递`48`
        admin_refunded_info = {
            "refunded_address": "退款收货地址",
            "refunded_name": "退款收货人",
            "refunded_phone": "退款联系电话",
            "remark": "备注"
        }
        
    """
    queryset = Order.objects.filter(order_type=OrderType.market,
                                    order_status__in=refund_status).order_by('-id')
    serializer_class = serializers.MarketRefundedSerializer
    filter_class = filters.OrderFilter
    permission_classes = (PermsRequired('main.refunded'),)

    def perform_update(self, serializer):
        serializer.save(operator_name=self.request.user.staffprofile)

    def get_serializer_class(self):
        if self.action == 'retry':
            return serializers.MarketOrderRetryRefundedSerializer
        elif self.action == 'deal_apply':
            return serializers.MarketRefundedApplySerializer
        return self.serializer_class

    @detail_route(methods=['POST'])
    def retry(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @detail_route(methods=['POST'])
    def deal_apply(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
