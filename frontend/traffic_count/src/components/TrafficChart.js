import { CartesianGrid, BarChart, Line, XAxis, YAxis, Tooltip, Bar,
         ResponsiveContainer } from 'recharts';


const formatTimestamps = (timestamp_in_seconds) => {
  let date = new Date(timestamp_in_seconds * 1000.0);
  return date.toLocaleTimeString("en-US", {timeZone: "America/New_York"});
}

function TrafficChart(props) {

  let data = props.data;
  data.forEach(x => {
    x.timestamp_in_seconds = Date.parse(x.timestamp + "Z") / 1000.0;
  });
  
  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <Bar stroke="#8884d8" dataKey="vehicles" />
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
        <XAxis
          dataKey="timestamp_in_seconds"
          type="number"
          domain={['auto', 'auto']}
          tickFormatter={formatTimestamps}/>
        <YAxis label={{ value: "Vehicles Detected in Frame", angle: -90 }}/>
        <Tooltip
          formatter={(value) => [value, "Vehicles"]}
          labelFormatter={formatTimestamps}/>
      </BarChart>
    </ResponsiveContainer>
  );
}

export default TrafficChart;