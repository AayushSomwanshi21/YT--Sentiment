import React from 'react'
import { PieChart, Pie, Cell, Legend, Tooltip } from "recharts";

const SentimentPieChart = ({ data }) => {

    const chartData = [
        { name: "Positive Comments", value: data.positive_comments || 0 },
        { name: "Negative Comments", value: data.negative_comments || 0 },
    ];

    const COLORS = ["#4caf50", "#f44336"];


    return (
        <div style={{ textAlign: "center", marginTop: "2rem" }}>
            <h2 style={{ color: "white" }}>Sentiment Distribution</h2>
            <PieChart width={800} height={400}>
                <Pie
                    data={chartData}
                    cx="50%"
                    cy="50%"
                    label={({ name, value }) => `${name}: ${value}`}
                    outerRadius={150}
                    fill="#8884d8"
                    dataKey="value"
                >
                    {chartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Pie>
                <Tooltip />
                <Legend />
            </PieChart>
        </div>
    )
}

export default SentimentPieChart