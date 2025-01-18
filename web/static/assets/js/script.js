function searchProtein() {
    const searchType = document.getElementById('search-type').value; // 获取检索方式
    const searchInput = document.getElementById('search-input').value; // 获取用户输入
    const species = document.getElementById('species').value; // 获取选择的物种

    // 检查输入值
    if (searchInput && species) {
        let url = '';
        if (searchType === 'protein_id') {
            // 如果选择了蛋白ID检索
            url = `http://127.0.0.1:5000/basic-info-search?search_type=protein_id&protein=${searchInput}&species=${species}`;
        } else if (searchType === 'sequence') {
            // 如果选择了蛋白序列检索
            url = `http://127.0.0.1:5000/basic-info-search?search_type=sequence&protein=${searchInput}&species=${species}`;
        }

        // 发起API请求
        fetch(url, {
            method: 'GET',
            mode: 'cors'  // 指定为跨域请求
        })
            .then(response => response.json())
            .then(data => {
                const proteinInfoDiv = document.getElementById('protein-info');

                if (data && data.protein_id) {
                    // 确保 GO Terms 存在且为数组
                    const goTerms = Array.isArray(data.go_terms) ? data.go_terms : [];

                    // 构建表格格式的蛋白信息和GO Terms信息
                    let resultHTML = `
                    <div class="protein-info">
                        <h3>Protein ID: ${data.protein_id}</h3>
                        <table>
                            <tr>
                                <th>Species</th>
                                <td>${data.species}</td>
                            </tr>
                            <tr>
                                <th>Primary Structure</th>
                                <td>${data.primary_structure}</td>
                            </tr>
                            <tr>
                                <th>Secondary Structure</th>
                                <td>${data.secondary_structure}</td>
                            </tr>
                            <tr>
                                <th>Tertiary Structure</th>
                                <td><a href="${data.tertiary_structure}" target="_blank">Link</a></td>
                            </tr>
                        </table>
                    </div>
                    <div class="go-terms">
                        <h4>GO Terms:</h4>
                        <table>
                            <thead>
                                <tr>
                                    <th>GO Term ID</th>
                                    <th>GO Term Name</th>
                                    <th>Category</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${goTerms.length > 0 ? goTerms.map(term => `
                                    <tr>
                                        <td>${term.id}</td>
                                        <td>${term.name}</td>
                                        <td>${term.category}</td>
                                    </tr>
                                `).join('') : '<tr><td colspan="3">No GO Terms available.</td></tr>'}
                            </tbody>
                        </table>
                    </div>
                `;

                    // 将构建的HTML插入到页面中
                    proteinInfoDiv.innerHTML = resultHTML;
                } else {
                    proteinInfoDiv.innerHTML = '<p>No results found for the given search criteria.</p>';
                }
            })
            .catch(error => {
                console.error('Error fetching protein data:', error);
                const proteinInfoDiv = document.getElementById('protein-info');
                proteinInfoDiv.innerHTML = '<p>Error fetching data. Please try again later.</p>';
            });
    } else {
        alert("Please enter Protein ID or Sequence, and select a species.");
    }
}



function searchGO() {
    const goTerm = document.getElementById('go-term').value;  // 获取用户输入的GO term
    console.log('Searching for GO Term:', goTerm);  // 打印用户输入的 GO Term

    if (goTerm) {
        const url = `http://127.0.0.1:5000/go-search/${goTerm}`;  // 发送GO term搜索请求
        console.log('Request URL:', url);  // 打印请求的 URL

        fetch(url, {
            method: 'GET',
            mode: 'cors'  // 指定为跨域请求
        })
            .then(response => {
                console.log('Response Status:', response.status);  // 打印响应的状态码
                return response.json();
            })
            .then(data => {
                console.log('Fetched GO Term Data:', data);  // 打印返回的数据

                const goInfoDiv = document.getElementById('go-info');

                if (data && data.basic_info) {
                    console.log('Data Received:', data);  // 确认返回的数据

                    const basicInfo = data.basic_info;  // 获取 basic_info 数据

                    // 构建结果显示的HTML
                    let resultHTML = `
                        <div class="go-term-result">
                            <h3>GO Term: ${basicInfo.id}</h3>
                            <p><strong>Name:</strong> ${basicInfo.name}</p>
                            <p><strong>Category:</strong> ${basicInfo.category}</p>
                            <p><strong>Description:</strong> ${basicInfo.description}</p>
                        </div>
                        <div class="go-interactions">
                            <h4>Outgoing Interactions:</h4>
                            <table>
                                <thead>
                                    <tr>
                                        <th>GO Term</th>
                                        <th>To GO Term</th>
                                        <th>Interaction Type</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${Array.isArray(data.outgoing_interactions) && data.outgoing_interactions.length > 0 ?
                            data.outgoing_interactions.map(interaction => `
                                            <tr>
                                                <td>${interaction.go_term}</td>
                                                <td>${interaction.to_go_term}</td>
                                                <td>${interaction.interaction_type}</td>
                                            </tr>
                                        `).join('') : '<tr><td colspan="3">No outgoing interactions available.</td></tr>'}
                                </tbody>
                            </table>

                            <h4>Incoming Interactions:</h4>
                            <table>
                                <thead>
                                    <tr>
                                        <th>GO Term</th>
                                        <th>From GO Term</th>
                                        <th>Interaction Type</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${Array.isArray(data.incoming_interactions) && data.incoming_interactions.length > 0 ?
                            data.incoming_interactions.map(interaction => `
                                            <tr>
                                                <td>${interaction.go_term}</td>
                                                <td>${interaction.from_go_term}</td>
                                                <td>${interaction.interaction_type}</td>
                                            </tr>
                                        `).join('') : '<tr><td colspan="3">No incoming interactions available.</td></tr>'}
                                </tbody>
                            </table>
                        </div>
                    `;

                    goInfoDiv.innerHTML = resultHTML;
                } else {
                    console.log('No basic_info found in response data.');  // 如果没有找到 basic_info 字段
                    goInfoDiv.innerHTML = '<p>No results found for the given GO Term.</p>';
                }
            })
            .catch(error => {
                console.error('Error fetching GO term data:', error);  // 捕获并打印错误
                const goInfoDiv = document.getElementById('go-info');
                goInfoDiv.innerHTML = '<p>Error fetching data. Please try again later.</p>';
            });
    } else {
        alert("Please enter a GO Term.");
    }
}

function searchInteraction() {
    console.log('Function Triggered')
    const proteinId = document.getElementById('protein-id').value;
    const species = document.getElementById('species').value;
    const minScore = document.getElementById('min-score').value;

    // 输出日志，检查输入参数
    console.log("Searching for interactions with Protein ID:", proteinId, "Species:", species, "Min Score:", minScore);

    if (proteinId && species) {
        const url = `http://127.0.0.1:5000/interaction-search?protein=${proteinId}&species=${species}&min_score=${minScore}`;

        // 输出日志，查看生成的请求URL
        console.log("Request URL:", url);

        fetch(url, {
            method: 'GET',
            mode: 'cors'  // 指定为跨域请求
        })
            .then(response => {
                // 输出响应状态
                console.log("Response Status:", response.status);
                return response.json();
            })
            .then(data => {
                // 输出接收到的数据
                console.log("Fetched Interaction Data:", data);

                const interactionInfoDiv = document.getElementById('interaction-info');

                if (data && data.interactions && data.interactions.length > 0) {
                    interactionInfoDiv.innerHTML = `
                    <h3>Protein: ${data.protein}</h3>
                    <p>Species: ${data.species}</p>
                    <h4>Interactions:</h4>
                    <ul>
                        ${data.interactions.map(interaction => `
                            <li>
                                <strong>Protein A:</strong> ${interaction.protein_a}, 
                                <strong>Protein B:</strong> ${interaction.protein_b}, 
                                <strong>Interaction Score:</strong> ${interaction.interaction_score}
                                <ul>
                                    ${interaction.validations.map(validation => `
                                        <li><strong>Experiment:</strong> ${validation.experiment_approach}, 
                                            <strong>PubMed ID:</strong> <a href="https://pubmed.ncbi.nlm.nih.gov/${validation.pubmed_id.replace('PUBMED:', '')}" target="_blank">${validation.pubmed_id.replace('PUBMED:', '')}</a>
                                        </li>
                                    `).join('')}
                                </ul>
                            </li>
                        `).join('')}
                    </ul>
                `;

                    // 输出日志，查看交互数据是否正确渲染
                    console.log("Interaction Info Rendered:", interactionInfoDiv.innerHTML);

                    // Display interaction network graph if available
                    if (data.graph_svg) {
                        const graphContainer = document.getElementById('interaction-network');
                        graphContainer.innerHTML = ''; // 清空容器内容，以防多余的文字或元素
                        graphContainer.innerHTML = `<img src=${data.graph_svg}`;
                        console.log("Interaction Network Graph Displayed.");
                    }
                } else {
                    interactionInfoDiv.innerHTML = '<p>No interaction data found for the given protein and species.</p>';
                    console.log("No interactions found.");
                }
            })
    } else {
        alert("Please enter Protein ID and select Species.");
        console.log("Missing Protein ID or Species.");
    }
}





