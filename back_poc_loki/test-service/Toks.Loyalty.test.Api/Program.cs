const string APP_NAME = "ARQUETIPO NET 6";

Log.Logger = new LoggerConfiguration()
                .MinimumLevel.Information()
                .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
                .MinimumLevel.Override("System", LogEventLevel.Warning)
                .WriteTo.Console()
                .CreateLogger();

try
{
    Log.Information($"{APP_NAME} service starting.");
    WebApplication.CreateBuilder(args)
    .AppConfiguration()
    .UseApplication()
    .Run();
}
catch (Exception ex)
{
    Log.Fatal(ex, $"{APP_NAME} service failed to start.");
}
finally
{
    Log.CloseAndFlush();
}