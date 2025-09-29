import React from "react";
import Menu from "./Menu";
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,} from "recharts";
import "./graficas.css";

const data = [
    { year: "2018", cop_usd: 3000, cop_eur: 2900 },
    { year: "2019", cop_usd: 3200, cop_eur: 3300 },
    { year: "2020", cop_usd: 0, cop_eur: 0 },
    { year: "2021", cop_usd: 3800, cop_eur: 3700 },
    { year: "2022", cop_usd: 3900, cop_eur: 4100 },
    { year: "2023", cop_usd: 5188, cop_eur: 4300 },
];

export default function Graficas() {
    return (
        <div className="graficas-page">
            <Menu />    
            <div className="graficas-content">
                <div className="graficas-header">
                    <h2>Gráficas</h2>
                </div>    
                <div className="monedas">
                    <div className="moneda-card">
                        <img src="/img/cop.png" alt="COP" />
                        <span>COP</span>
                    </div>
                    <div className="moneda-card">
                        <img src="/img/usd.png" alt="USD" />
                        <span>USD</span>
                    </div>
                    <div className="moneda-card">
                        <img src="/img/eur.png" alt="EUR" />
                        <span>EUR</span>
                    </div>
                </div>    
                <div className="graficas-main">
                    <div className="chart-container">
                        <ResponsiveContainer width="100%" height={380}>
                            <LineChart data={data}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#2b2b2b" />
                                <XAxis dataKey="year" stroke="#9ca3af" />
                                <YAxis stroke="#9ca3af" />
                                <Tooltip />
                                <Legend />
                                <Line
                                    type="monotone"
                                    dataKey="cop_usd"
                                    stroke="#00c0ff"
                                    dot={{ r: 4 }}
                                    name="COP/USD"
                                />
                                <Line
                                    type="monotone"
                                    dataKey="cop_eur"
                                    stroke="#f1c40f"
                                    dot={{ r: 4 }}
                                    name="COP/EUR"
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>  
                </div>
            </div>
        </div>
    );
}
