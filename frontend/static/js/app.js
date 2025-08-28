// 全局变量
let toast;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function () {
    // 初始化Toast
    toast = new bootstrap.Toast(document.getElementById('responseToast'));

    // 设置默认时间范围
    setDefaultDateRange();

    // 加载初始服务信息
    refreshServiceInfo();

    // 定期刷新服务信息
    setInterval(() => {
        refreshServiceInfo();
    }, 30000); // 每30秒刷新一次
});

// 显示消息提示
function showMessage(message, type = 'info') {
    const toastElement = document.getElementById('responseToast');
    const toastBody = document.getElementById('toastMessage');

    toastBody.textContent = message;

    // 根据类型设置样式
    toastElement.className = `toast ${type === 'error' ? 'bg-danger text-white' : type === 'success' ? 'bg-success text-white' : 'bg-info text-white'}`;

    toast.show();
}

// 健康检查
async function checkHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();

        if (response.ok) {
            showMessage(`服务状态: ${data.status} - ${data.message}`, 'success');
            // 更新服务状态显示
            document.getElementById('serviceStatus').textContent = '运行中';
            document.getElementById('serviceStatus').className = 'text-success';
        } else {
            showMessage('服务检查失败', 'error');
            document.getElementById('serviceStatus').textContent = '异常';
            document.getElementById('serviceStatus').className = 'text-danger';
        }
    } catch (error) {
        showMessage(`连接错误: ${error.message}`, 'error');
        document.getElementById('serviceStatus').textContent = '连接失败';
        document.getElementById('serviceStatus').className = 'text-danger';
    }
}

// 刷新服务信息
async function refreshServiceInfo() {
    try {
        // 获取健康检查信息
        const healthResponse = await fetch('/api/health');
        const healthData = await healthResponse.json();

        if (healthResponse.ok) {
            // 更新服务状态
            document.getElementById('serviceStatus').textContent = '运行中';
            document.getElementById('serviceStatus').className = 'text-success';

            // 更新服务器时间
            const serverTime = new Date(healthData.timestamp);
            document.getElementById('serverTime').textContent = serverTime.toLocaleString('zh-CN');

            // 更新最后更新时间
            const now = new Date();
            document.getElementById('lastUpdate').textContent = now.toLocaleString('zh-CN');
        } else {
            document.getElementById('serviceStatus').textContent = '异常';
            document.getElementById('serviceStatus').className = 'text-danger';
            document.getElementById('serverTime').textContent = '--';
        }
    } catch (error) {
        console.error('刷新服务信息失败:', error);
        document.getElementById('serviceStatus').textContent = '连接失败';
        document.getElementById('serviceStatus').className = 'text-danger';
        document.getElementById('serverTime').textContent = '--';
    }
}

// 仿真数据生成函数

// 生成周计划数据
async function generateWeeklyPlan() {
    try {
        showMessage('正在生成周计划数据...', 'info');

        // 使用配置的时间范围
        const dateRange = getCurrentDateRange();

        const response = await fetch('/api/generate/all-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dateRange)
        });

        const result = await response.json();

        if (result.success) {
            const data = result.data;
            showMessage(`周计划数据生成成功！共生成 ${data.weeks_plan_num} 个周计划`, 'success');

            // 更新周计划状态
            document.getElementById('weeklyPlanStatus').textContent = `已生成 (${data.weeks_plan_num}个周计划)`;
            document.getElementById('weeklyPlanStatus').className = 'text-success';

            // 更新统计数据
            document.getElementById('weeksPlanCount').textContent = data.weeks_plan_num;

            // 在控制台显示生成的数据
            console.log('周计划数据:', data);
        } else {
            showMessage(`生成失败: ${result.message}`, 'error');
            document.getElementById('weeklyPlanStatus').textContent = '生成失败';
            document.getElementById('weeklyPlanStatus').className = 'text-danger';
        }
    } catch (error) {
        showMessage(`生成错误: ${error.message}`, 'error');
        document.getElementById('weeklyPlanStatus').textContent = '生成失败';
        document.getElementById('weeklyPlanStatus').className = 'text-danger';
    }
}

// 生成班组数据
async function generateTeamData() {
    try {
        showMessage('正在生成班组数据...', 'info');

        // 使用配置的时间范围
        const dateRange = getCurrentDateRange();

        const response = await fetch('/api/generate/all-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dateRange)
        });

        const result = await response.json();

        if (result.success) {
            const data = result.data;
            showMessage(`班组数据生成成功！共生成 ${data.team_num} 个班组`, 'success');

            // 更新班组状态
            document.getElementById('teamDataStatus').textContent = `已生成 (${data.team_num}个班组)`;
            document.getElementById('teamDataStatus').className = 'text-success';

            // 更新统计数据
            document.getElementById('teamCount').textContent = data.team_num;

            console.log('班组数据:', data);
        } else {
            showMessage(`生成失败: ${result.message}`, 'error');
            document.getElementById('teamDataStatus').textContent = '生成失败';
            document.getElementById('teamDataStatus').className = 'text-danger';
        }
    } catch (error) {
        showMessage(`生成错误: ${error.message}`, 'error');
        document.getElementById('teamDataStatus').textContent = '生成失败';
        document.getElementById('teamDataStatus').className = 'text-danger';
    }
}

// 生成班组人员数据
async function generateTeamMemberData() {
    try {
        showMessage('正在生成班组人员数据...', 'info');

        // 使用配置的时间范围
        const dateRange = getCurrentDateRange();

        const response = await fetch('/api/generate/all-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dateRange)
        });

        const result = await response.json();

        if (result.success) {
            const data = result.data;
            showMessage(`班组人员数据生成成功！共生成 ${data.team_people_num} 个人员`, 'success');

            // 更新班组人员状态
            document.getElementById('teamMemberDataStatus').textContent = `已生成 (${data.team_people_num}个人员)`;
            document.getElementById('teamMemberDataStatus').className = 'text-success';

            // 更新统计数据
            document.getElementById('teamPeopleCount').textContent = data.team_people_num;

            console.log('班组人员数据:', data);
        } else {
            showMessage(`生成失败: ${result.message}`, 'error');
            document.getElementById('teamMemberDataStatus').textContent = '生成失败';
            document.getElementById('teamMemberDataStatus').className = 'text-danger';
        }
    } catch (error) {
        showMessage(`生成错误: ${error.message}`, 'error');
        document.getElementById('teamMemberDataStatus').textContent = '生成失败';
        document.getElementById('teamMemberDataStatus').className = 'text-danger';
    }
}

// 生成风险底数一本账数据
async function generateRiskData() {
    try {
        showMessage('正在生成风险底数一本账数据...', 'info');

        // 使用配置的时间范围
        const dateRange = getCurrentDateRange();

        const response = await fetch('/api/generate/all-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dateRange)
        });

        const result = await response.json();

        if (result.success) {
            const data = result.data;
            showMessage(`风险底数一本账数据生成成功！共生成 ${data.risk_precaution_num} 个风险项`, 'success');

            // 更新风险数据状态
            document.getElementById('riskDataStatus').textContent = `已生成 (${data.risk_precaution_num}个风险项)`;
            document.getElementById('riskDataStatus').className = 'text-success';

            // 更新统计数据
            document.getElementById('riskPrecautionCount').textContent = data.risk_precaution_num;

            console.log('风险底数一本账数据:', data);
        } else {
            showMessage(`生成失败: ${result.message}`, 'error');
            document.getElementById('riskDataStatus').textContent = '生成失败';
            document.getElementById('riskDataStatus').className = 'text-danger';
        }
    } catch (error) {
        showMessage(`生成错误: ${error.message}`, 'error');
        document.getElementById('riskDataStatus').textContent = '生成失败';
        document.getElementById('riskDataStatus').className = 'text-danger';
    }
}

// 批量生成所有数据
async function generateAllData() {
    try {
        showMessage('正在批量生成所有仿真数据...', 'info');

        // 使用配置的时间范围
        const dateRange = getCurrentDateRange();

        const response = await fetch('/api/generate/all-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dateRange)
        });

        const result = await response.json();

        if (result.success) {
            const data = result.data;
            const summary = `周计划: ${data.weeks_plan_num}个, 班组: ${data.team_num}个, 人员: ${data.team_people_num}个, 风险: ${data.risk_precaution_num}个`;

            showMessage(`所有仿真数据生成成功！${summary}`, 'success');

            // 更新所有模块状态
            document.getElementById('weeklyPlanStatus').textContent = `已生成 (${data.weeks_plan_num}个周计划)`;
            document.getElementById('weeklyPlanStatus').className = 'text-success';

            document.getElementById('teamDataStatus').textContent = `已生成 (${data.team_num}个班组)`;
            document.getElementById('teamDataStatus').className = 'text-success';

            document.getElementById('teamMemberDataStatus').textContent = `已生成 (${data.team_people_num}个人员)`;
            document.getElementById('teamMemberDataStatus').className = 'text-success';

            document.getElementById('riskDataStatus').textContent = `已生成 (${data.risk_precaution_num}个风险项)`;
            document.getElementById('riskDataStatus').className = 'text-success';

            console.log('所有仿真数据:', data);
        } else {
            showMessage(`批量生成失败: ${result.message}`, 'error');
        }
    } catch (error) {
        showMessage(`批量生成错误: ${error.message}`, 'error');
    }
}

// 设置默认时间范围
function setDefaultDateRange() {
    const now = new Date();
    const startTime = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000); // 一周前
    const endTime = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000); // 一周后

    document.getElementById('startDate').value = startTime.toISOString().split('T')[0];
    document.getElementById('endDate').value = endTime.toISOString().split('T')[0];
}

// 获取当前配置的时间范围
function getCurrentDateRange() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    if (!startDate || !endDate) {
        setDefaultDateRange();
        return {
            plan_start_time: document.getElementById('startDate').value,
            plan_end_time: document.getElementById('endDate').value
        };
    }

    return {
        plan_start_time: startDate,
        plan_end_time: endDate
    };
}


// 加载数据库配置
async function loadDbConfig() {
    const response = await fetch('/api/db/config', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    const result = await response.json();
    console.log(result)
    if (result.success) {
        const data = result.data;
        document.getElementById('dbHost').value = data.host
        document.getElementById('dbPort').value = data.port
        document.getElementById('dbName').value = data.database
        document.getElementById('dbUser').value = data.user
        document.getElementById('dbPwd').value = data.password

    }
    showMessage('数据配置信息加载完成', 'info')
}

// 保存数据库配置
async function saveDbConfig() {
    const host = document.getElementById('dbHost').value;
    const port = document.getElementById('dbPort').value;
    const database = document.getElementById('dbName').value;
    const user = document.getElementById('dbUser').value;
    const password = document.getElementById('dbPwd').value;
    const dbInfo = {
        host: host,
        port: port,
        user: user,
        password: password,
        database: database
    }
    const response = await fetch('/api/db/config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dbInfo)
    })
    const result = await response.json();

    if (result.success) {
        const data = result.data;
    }
    showMessage('数据库信息保存成功', 'info')
}

// 测试数据库连接
async function testDbConnection() {
    const response = await fetch('/api/db/connect/test', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    const result = await response.json();
    console.log(result)
    if (result.success) {
        const data = result.data;
        if (data.connected) {
            showMessage('数据库连接成功', 'info')
        } else {
            showMessage('数据库连接失败: ' + data.err, 'error')
        }

    }

}

// 监听网络状态变化
window.addEventListener('online', () => {
    showMessage('网络连接已恢复', 'success');
});

window.addEventListener('offline', () => {
    showMessage('网络连接已断开', 'error');
});

document.addEventListener('DOMContentLoaded', function () {
    // 你的代码直接写在这里
    loadDbConfig()
});
