import { CartesianGrid, LineChart, Line, XAxis, Tooltip, ResponsiveContainer } from 'recharts';

function TrafficChart(props) {
  const formatTimestamps = (timestamp_in_seconds) => {
    let date = new Date(timestamp_in_seconds * 1000.0);
    return date.toLocaleTimeString();
  }
  let data = props.data;
  data.forEach(x => {
    x.timestamp_in_seconds = new Date(x.timestamp).getTime() / 1000.0;
  });
  
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <Line type="monotone" stroke="#8884d8" dataKey="vehicles" />
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
        <XAxis
          dataKey="timestamp_in_seconds"
          type="number"
          domain={['auto', 'auto']}
          tickFormatter={formatTimestamps}/>
        <Tooltip labelFormatter={formatTimestamps}/>
      </LineChart>
    </ResponsiveContainer>
  );
}

export default TrafficChart;