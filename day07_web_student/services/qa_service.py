from pathlib import Path

import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    normalized = question.replace(" ", "").lower()

    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"
    # TODO 4-1：补充“流失率”“偏好品类”“生命周期风险”和“订单”四类问答。
    # 每个回答都必须引用data目录中已经计算的指标，不得编造数值。
    if any(word in normalized for word in ["流失率", "流失人数", "流失多少人"]):
        total_user = int(metrics["用户数"])
        churn_user = int(metrics["流失人数"])
        churn_rate = float(metrics["流失率"]) * 100
        return f"总流失用户为{churn_user:,}人，整体流失率为{churn_rate:.1f}%。"

    if any(word in normalized for word in ["哪个品类用户最多", "偏好品类", "用户最多的品类"]):
        max_cat_row = category_df.loc[category_df["用户数"].idxmax()]
        cat_name = max_cat_row["PreferedOrderCat"]
        cat_user = int(max_cat_row["用户数"])
        return f"用户数量最多的偏好品类是「{cat_name}」，共有{cat_user:,}名用户。"

    if any(word in normalized for word in ["哪个阶段风险最高", "生命周期", "流失风险最高"]):
        max_seg_row = segment_df.loc[segment_df["流失率"].idxmax()]
        seg_name = max_seg_row["TenureGroup"]
        seg_rate = float(max_seg_row["流失率"]) * 100
        return f"流失风险最高的生命周期阶段为「{seg_name}」，该阶段流失率达到{seg_rate:.1f}%。"

    if any(word in normalized for word in ["平均订单数", "订单均值", "订单中位数"]):
        avg_order = float(metrics["平均订单数"])
        # 从品类表计算全量订单中位数
        median_order = category_df["平均订单数"].median()
        return f"用户平均订单数均值为{avg_order:.2f}单/人，全品类订单数中位数为{median_order:.2f}单/人。"

    return (
        "基础问答尚未完成。目前支持：总用户数、总体流失情况、用户最多偏好品类、最高风险生命周期阶段、平均订单数据；"
        "请换一种更具体的问法。"
    )
