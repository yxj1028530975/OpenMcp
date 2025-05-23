from pydantic import Field
from typing import List, Optional, Dict, Any, Union, Annotated
import httpx
from common.server import server_app
from dataclasses import dataclass
import tomllib
import datetime


with open("apps/application/odoo_data/config.toml", "rb") as f:
    plugin_config = tomllib.load(f)

base_url = plugin_config["odoo_data"]["base_url"]

def _validate_date(date_str: Optional[str]) -> Optional[str]:
    if date_str is None:
        return None
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError(f"日期格式错误: {date_str}，应为 YYYY-MM-DD")

@server_app.tool()
async def search_quality_data(
    factory_code: Optional[str] = None,
    factory_name: Optional[str] = None,
    discoverer_code: Optional[str] = None,
    discoverer_name: Optional[str] = None,
    responsible_department: Optional[str] = None,
    discovery_location: Optional[str] = None,
    issue_subtype: Optional[str] = None,
    sequence_number: Optional[str] = None,
    production_category: Optional[Union[str, List[str]]] = None,
    issue_type: Optional[Union[str, List[str]]] = None,
    issue_level: Optional[Union[str, List[str]]] = None,
    state: Optional[Union[str, List[str]]] = None,
    discovery_date_start: Optional[str] = None,
    discovery_date_end: Optional[str] = None,
    planned_completion_date_start: Optional[str] = None,
    planned_completion_date_end: Optional[str] = None,
    import_date_start: Optional[str] = None,
    import_date_end: Optional[str] = None,
    search_text: Optional[str] = None,
    offset: int = 0,
    limit: int = 80,
    order: str = "discovery_date desc, id desc",
) -> Dict[str, Any]:
    """
        质量数据查询接口
        
        基本信息:
        - 接口地址: /quality/data/search
        - 请求方式: POST
        - Content-Type: application/json
        - 认证方式: public（无需认证）
        
        请求参数:
        1. 基础查询参数:
            - factory_code (string, 选填): 工厂代码，如 "F001"
            - factory_name (string, 选填): 工厂名称，如 "上海工厂"
            - discoverer_code (string, 选填): 发现人员工号，如 "EMP001"
            - discoverer_name (string, 选填): 发现人姓名，如 "张三"
            - responsible_department (string, 选填): 责任部门，如 "生产部"
            - discovery_location (string, 选填): 发现地点，如 "车间A"
            - issue_subtype (string, 选填): 问题类型子类，如 "设备故障"
            - sequence_number (string, 选填): 序号，如 "1"
            
        2. 分类查询参数:
            - production_category (array/string, 选填): 生产分类
                可选值: ["solid", "freeze_dry", "injection", "engineering", "warehouse", "qc"]
                说明: solid(固体), freeze_dry(冻干), injection(水针), engineering(工程), warehouse(仓库), qc(QC)
            - issue_type (array/string, 选填): 问题类型
                可选值: ["personnel", "equipment", "material", "method", "environment", "detection", "other"]
                说明: personnel(人), equipment(机), material(物料), method(法), environment(环), detection(检测/计量), other(其他)
            - issue_level (array/string, 选填): 问题等级
                可选值: ["critical", "major", "minor"]
                说明: critical(严重), major(主要), minor(次要)
            - state (array/string, 选填): 状态
                可选值: ["draft", "confirmed", "in_progress", "done", "cancelled"]
                说明: draft(草稿), confirmed(已确认), in_progress(处理中), done(已完成), cancelled(已取消)
                
        3. 时间范围查询参数:
            - discovery_date_start (string, 选填): 发现时间开始，格式: "YYYY-MM-DD"
            - discovery_date_end (string, 选填): 发现时间结束，格式: "YYYY-MM-DD"
            - planned_completion_date_start (string, 选填): 计划完成时间开始，格式: "YYYY-MM-DD"
            - planned_completion_date_end (string, 选填): 计划完成时间结束，格式: "YYYY-MM-DD"
            - import_date_start (string, 选填): 导入时间开始，格式: "YYYY-MM-DD"
            - import_date_end (string, 选填): 导入时间结束，格式: "YYYY-MM-DD"
            
        4. 搜索和分页参数:
            - search_text (string, 选填): 模糊搜索关键词，会搜索以下字段:
                * 问题描述(issue_description)
                * 整改措施(corrective_action)
                * 整改完成情况(correction_status)
                * 事件发生过程(event_process)
                * 备注(notes)
            - offset (integer, 选填): 分页起始位置，默认: 0
            - limit (integer, 选填): 每页记录数，默认: 80，建议不超过100
            - order (string, 选填): 排序方式，默认: "discovery_date desc, id desc"
            
        返回数据:
        成功响应 (code: 200):
        {
            "code": 200,
            "message": "查询成功",
            "data": {
                "total": 100,          // 总记录数
                "items": [             // 数据列表
                    {
                        "id": 1,                           // 记录ID
                        "factory_code": "F001",            // 工厂代码
                        "factory_name": "上海工厂",         // 工厂名称
                        "discoverer_code": "EMP001",       // 发现人员工号
                        "discoverer_name": "张三",          // 发现人姓名
                        "discovery_date": "2024-03-20",    // 发现时间
                        "responsible_department": "生产部",  // 责任部门
                        "discovery_location": "车间A",      // 发现地点
                        "production_category": "固体部门",   // 生产分类
                        "issue_description": "问题描述",     // 问题描述
                        "issue_type": "equipment",         // 问题类型
                        "issue_subtype": "设备故障",        // 问题子类
                        "corrective_action": "整改措施",     // 整改措施
                        "planned_completion_date": "2024-03-25", // 计划完成时间
                        "correction_status": "已完成",       // 整改状态
                        "event_process": "事件过程",         // 事件过程
                        "discovery_area": "洁净区",          // 发现区域
                        "deviation_record": "DEV001",       // 偏差记录
                        "issue_level": "major",            // 问题等级
                        "state": "done",                   // 状态
                        "sequence_number": "1",            // 序号
                        "import_date": "2024-03-20 10:00:00" // 导入时间
                    }
                ]
            }
        }
        
        错误响应 (code: 500):
        {
            "code": 500,
            "message": "查询失败: 具体错误信息",
            "data": null
        }
        
        使用示例:
        1. 基础查询:
        {
            "factory_code": "F001",
            "limit": 10
        }
        
        2. 多条件组合查询:
        {
            "production_category": ["solid", "freeze_dry"],
            "discovery_date_start": "2024-01-01",
            "discovery_date_end": "2024-03-20",
            "issue_level": "major",
            "search_text": "质量问题",
            "limit": 20,
            "offset": 0
        }
        
        3. 模糊搜索:
        {
            "search_text": "设备故障",
            "limit": 50
        }
        
        注意事项:
        1. 所有时间字段格式必须为 "YYYY-MM-DD"
        2. 模糊搜索会同时搜索多个字段，可能影响查询性能
        3. 分类字段支持单个值或数组形式
        4. 接口返回的时间字段格式:
           - 日期字段: YYYY-MM-DD
           - 时间字段: YYYY-MM-DD HH:mm:ss
        5. 所有查询条件都是可选的，可以根据需要组合使用
        6. 排序字段支持多个字段组合，格式为 "字段1 排序方式, 字段2 排序方式"
        
    """
    # 时间参数校验
    for key in [
        "discovery_date_start", "discovery_date_end",
        "planned_completion_date_start", "planned_completion_date_end",
        "import_date_start", "import_date_end"
    ]:
        if locals()[key]:
            try:
                _validate_date(locals()[key])
            except ValueError as e:
                return {"code": 400, "message": str(e), "data": None}

    # 构造请求参数
    payload = {
        "factory_code": factory_code,
        "factory_name": factory_name,
        "discoverer_code": discoverer_code,
        "discoverer_name": discoverer_name,
        "responsible_department": responsible_department,
        "discovery_location": discovery_location,
        "issue_subtype": issue_subtype,
        "sequence_number": sequence_number,
        "production_category": production_category,
        "issue_type": issue_type,
        "issue_level": issue_level,
        "state": state,
        "discovery_date_start": discovery_date_start,
        "discovery_date_end": discovery_date_end,
        "planned_completion_date_start": planned_completion_date_start,
        "planned_completion_date_end": planned_completion_date_end,
        "import_date_start": import_date_start,
        "import_date_end": import_date_end,
        "search_text": search_text,
        "offset": offset,
        "limit": limit,
        "order": order,
    }
    # 移除值为 None 的参数
    payload = {k: v for k, v in payload.items() if v is not None}

    url = f"{base_url}/quality/data/search"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        return {"code": 500, "message": f"请求异常: {str(e)}", "data": None}
    except httpx.HTTPStatusError as e:
        return {"code": response.status_code, "message": f"HTTP错误: {str(e)}", "data": None}
    except Exception as e:
        return {"code": 500, "message": f"未知错误: {str(e)}", "data": None}

