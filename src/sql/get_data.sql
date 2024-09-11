select
    {fields}
from
    dip.tb_trace_rebuild t
where
    1=1
    and (t.`异常类型` in ({anomalies}) or t.`异常类型`='nan')
    