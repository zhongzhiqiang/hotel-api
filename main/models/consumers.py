# coding:utf-8
from __future__ import unicode_literals

from django.db import models


class Consumer(models.Model):
    # 消费者的username为用户昵称或者账号。

    SEX_STATUS = (
        (10, '为止'),
        (20, '男'),
        (30, '女')
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

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = '消费者信息'
        verbose_name_plural = verbose_name


class DistributionApply(models.Model):

    APPLY_STATUS = (
        (10, '提交成功'),
        (20, '受理中'),
        (30, '受理完成'),
        (40, '撤回申请')
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
        blank=True
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

    class Meta:
        verbose_name = '分销申请记录'
        verbose_name_plural = verbose_name


class DistributionBonus(models.Model):
    consumer = models.OneToOneField(
        'main.Consumer',
        related_name='distribution_bonus',
        on_delete=models.SET_NULL,
        null=True
    )
    bonus = models.DecimalField(
        '分销奖金',
        max_digits=10,
        decimal_places=2
    )
    operator_time = models.DateTimeField(
        '操作时间',
        auto_now=True,
        blank=True
    )

    class Meta:
        verbose_name = '分销奖金'
        verbose_name_plural = verbose_name


class DistributionBonusDetail(models.Model):
    DETAIL_STATUS = (
        (10, '未知'),
        (20, '成功'),
        (30, '失败'),
        (40, '取消'),
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
    bonus_detail = models.DecimalField(
        '使用金额',
        max_digits=10,
        decimal_places=2
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

    class Meta:
        verbose_name = '提取分销金额申请'
        verbose_name_plural = verbose_name
