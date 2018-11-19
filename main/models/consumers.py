# coding:utf-8
from __future__ import unicode_literals

import datetime

from django.db import models


class Consumer(models.Model):
    # 消费者的username为用户昵称或者账号。

    SEX_STATUS = (
        (10, '未知'),
        (20, '男'),
        (30, '女')
    )
    openid = models.CharField(
        '微信openid',
        max_length=100,
        blank=True,
        null=True
    )
    session_key = models.CharField(
        '微信回话key',
        max_length=100,
        blank=True,
        null=True
    )
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        verbose_name='用户'
    )
    phone = models.CharField(
        '联系电话',
        max_length=15,
        blank='',
        default='',
    )
    user_name = models.CharField(
        '用户姓名',
        max_length=30,
        default=''
    )
    avatar_url = models.CharField(
        "头像链接",
        default='',
        max_length=100
    )
    sex = models.IntegerField(
        '性别',
        choices=SEX_STATUS,
        default=10,
    )

    contact_addr = models.CharField(
        '联系地址',
        max_length=100,
        blank='',
        default=''
    )
    is_distribution = models.BooleanField(
        '是否为分销人员',
        default=False,
        blank=True
    )
    sell_user = models.ForeignKey(
        'main.Consumer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='推销人'
    )

    bonus = models.DecimalField(
        '分销奖金',
        max_digits=10,
        decimal_places=2,
        blank=True,
        default=0,
    )
    recharge_balance = models.DecimalField(
        '余额',
        max_digits=10,
        decimal_places=2,
        blank=True,
        default=0,
        help_text='充值余额'
    )
    free_balance = models.DecimalField(
        '奖励金',
        max_digits=10,
        decimal_places=2,
        blank=True,
        default=0,
        help_text='充值赠送金额'
    )

    @property
    def balance(self):
        return self.recharge_balance + self.free_balance

    @property
    def order_count(self):
        return self.order_set.count()

    @property
    def is_vip(self):
        if hasattr(self, 'vipmember'):
            return True
        return False

    @property
    def discount(self):
        if hasattr(self, 'vipmember'):
            return self.vipmember.discount
        return 1

    @property
    def integral(self):
        if hasattr(self, 'integral_info'):
            return self.integral_info.integral
        return 0

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = '客户信息'
        verbose_name_plural = verbose_name


class ConsumerBalance(models.Model):
    # 用户消费记录
    BalanceType = (
        (10, '增加'),
        (20, '消费'),
    )
    consumer = models.ForeignKey(
        'main.Consumer',
        verbose_name='对应用户',
    )
    balance_type = models.IntegerField(
        '余额类型',
        choices=BalanceType,
        default=10,
    )
    message = models.CharField(
        '消费备注',
        max_length=30,
        default=0,
    )
    cost_price = models.DecimalField(
        '消费金额',
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='正数代表为充值。负数代表消费'
    )
    create_time = models.DateTimeField(
        '消费时间',
        auto_now_add=True,
    )
    left_balance = models.DecimalField(
        '剩余余额',
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='用户剩余余额'
    )
    recharge = models.ForeignKey(
        'main.RechargeInfo',
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return '%s, %s' % (self.consumer, self.get_balance_type_display())

    class Meta:
        verbose_name = '用户余额详情'
        verbose_name_plural = verbose_name


class RechargeInfo(models.Model):
    RECHARGE_STATUS = (
        (10, '成功'),
        (20, '取消'),
        (30, '等待支付')
    )
    order_id = models.CharField(
        '充值订单号',
        max_length=20,
        blank=True,
        null=True,
        db_index=True
    )
    recharge_status = models.IntegerField(
        '充值状态',
        choices=RECHARGE_STATUS,
        default=30,
        blank=True,
    )
    recharge_money = models.DecimalField(
        '充值金额',
        max_digits=10,
        decimal_places=2,
    )
    free_money = models.DecimalField(
        '赠送金额',
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    consumer = models.ForeignKey(
        'main.Consumer',
        verbose_name='用户',
        blank=True,
        null=True
    )
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )
    pay_time = models.DateTimeField(
        '支付时间',
        blank=True,
        null=True
    )
    update_time = models.DateTimeField(
        '更新时间',
        auto_now=True
    )

    @property
    def balance(self):
        return self.recharge_money + self.free_money

    def make_order_id(self):
        return 'recharge%s%8.8d' % (datetime.date.today().strftime('%Y%m%d'), self.id)

    class Meta:
        verbose_name = '用户充值信息'
        verbose_name_plural = verbose_name


class DistributionApply(models.Model):

    APPLY_STATUS = (
        (10, '提交成功'),
        (20, '拒绝'),
        (30, '完成'),
        (40, '撤回申请'),
    )

    consumer = models.ForeignKey(
        'main.Consumer',
        null=True,
        on_delete=models.SET_NULL,
        help_text='用户',
        blank=True
    )
    apply_status = models.IntegerField(
        '申请状态',
        choices=APPLY_STATUS,
        default=10,
    )
    apply_time = models.DateTimeField(
        '申请时间',
        auto_now_add=True
    )
    apply_remark = models.CharField(
        '申请原因',
        max_length=520,
    )
    success_time = models.DateTimeField(
        '成功时间',
        null=True,
        blank=True
    )
    operator_time = models.DateTimeField(
        '操作时间',
        auto_now=True,
        blank=True,
        null=True
    )
    operator_name = models.ForeignKey(
        'main.StaffProfile',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    is_success = models.BooleanField(
        '是否申请成功',
        default=False,
        blank=True
    )

    fail_remark = models.CharField(
        '失败原因',
        blank=True,
        default='',
        max_length=200
    )

    def __unicode__(self):
        return self.consumer.user_name

    class Meta:
        verbose_name = '分销申请记录'
        verbose_name_plural = verbose_name


class DistributionBonusDetail(models.Model):
    DETAIL_STATUS = (
        (10, '未知'),
        (20, '成功'),
        (30, '失败'),
        (40, '取消'),
    )
    DETAIL_TYPE = (
        (0, '未知'),
        (10, '收入'),
        (20, '支出')
    )
    consumer = models.ForeignKey(
        'main.Consumer',
        related_name='distribution_bonus_detail',
        on_delete=models.SET_NULL,
        null=True
    )
    status = models.IntegerField(
        '状态',
        choices=DETAIL_STATUS,
        default=10,
        blank=True
    )
    detail_type = models.IntegerField(
        '类型',
        help_text='奖金明细类型',
        default=0
    )
    pick = models.ForeignKey(
        'main.DistributionBonusPick',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='提取关联申请'
    )
    last_bonus = models.DecimalField(
        '剩余奖金',
        max_digits=10,
        decimal_places=2
    )
    use_bonus = models.DecimalField(
        '使用金额',
        max_digits=10,
        decimal_places=2,
        help_text='消费金额'
    )
    remark = models.CharField(
        '使用原因',
        max_length=100,
    )
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )

    operator_time = models.DateTimeField(
        '操作时间',
        auto_now=True
    )

    operator_name = models.ForeignKey(
        'main.StaffProfile',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return self.consumer.user_name

    class Meta:
        verbose_name = '分销奖金明细'
        verbose_name_plural = verbose_name


class DistributionBonusPick(models.Model):

    PICK_STATUS = (
        (10, '提交申请'),
        (20, '正在处理'),
        (30, '转账中'),
        (40, '完成'),
        (50, '提取失败'),
        (60, '取消申请'),
    )

    consumer = models.ForeignKey(
        'main.Consumer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    pick_order = models.CharField(
        '提取订单号',
        max_length=20,
        blank=True,
        null=True,
        db_index=True,
        error_messages={
            'unique': "订单号错误"
        }
    )
    pick_status = models.IntegerField(
        '提取状态',
        choices=PICK_STATUS,
        default=10,
        blank=True,
    )
    pick_money = models.DecimalField(
        '提取金额',
        max_digits=10,
        decimal_places=2,
    )

    pick_time = models.DateTimeField(
        '提交时间',
        auto_now_add=True
    )
    success_time = models.DateTimeField(
        '完成时间',
        null=True,
        blank=True
    )
    transfer_time = models.DateTimeField(
        '转账时间',
        null=True,
        blank=True
    )

    fail_remark = models.CharField(
        '失败原因',
        null=True,
        blank=True,
        max_length=500,
        default=''
    )
    operator_time = models.DateTimeField(
        '操作时间',
        auto_now=True
    )
    operator_name = models.ForeignKey(
        'main.StaffProfile',
        verbose_name='操作人员',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def make_order_id(self):
        """创建工单号"""
        return 'pick%s%8.8d' % (datetime.date.today().strftime('%Y%m%d'), self.id)

    def __unicode__(self):
        return self.consumer.user_name

    class Meta:
        verbose_name = '提取分销金额申请'
        verbose_name_plural = verbose_name


class DistributionWXInfo(models.Model):

    distribution_pick = models.ForeignKey(
        'main.DistributionBonusPick',
        help_text='一个申请可能有多个转账'
    )
    wx_payment_no = models.CharField(
        '微信付款订单号',
        max_length=100,
        default='',
        blank=True,
        help_text='微信内部订单号'
    )
    distribution_order_id = models.CharField(
        '提取转账订单号',
        max_length=40,
        default='',
        blank=True,
        help_text='成功提取时的订单号'
    )
    wx_result_code = models.CharField(
        '微信业务结果',
        default='',
        max_length=20,
        blank=True
    )
    err_code = models.CharField(
        '微信错误代码',
        default='',
        max_length=30,
        blank=True
    )
    err_code_des = models.CharField(
        '微信错误描述',
        blank=True,
        default='',
        max_length=100
    )
    payment_time = models.DateTimeField(
        '微信到账时间',
        blank=True,
        null=True
    )
