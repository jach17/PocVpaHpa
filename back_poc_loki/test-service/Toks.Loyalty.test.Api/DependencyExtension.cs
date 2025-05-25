// <summary>
// <copyright file="DependencyExtension.cs" company="Axity">
// This source code is Copyright Axity and MAY NOT be copied, reproduced,
// published, distributed or transmitted to or stored in any manner without prior
// written consent from Axity (www.axity.com).
// </copyright>
// </summary>

namespace Toks.Loyalty.test.Api
{
    /// <summary>
    /// DependencyExtension static.
    /// </summary>
    public static class DependencyExtension
    {
        /// <summary>
        /// Config application.
        /// </summary>
        /// <param name="webApplication">WebApplicationBuilder.</param>
        /// <returns>WebApplication.</returns>
        public static WebApplication AppConfiguration(this WebApplicationBuilder webApplication)
        {
            webApplication.AddPlaceholderResolver();

            webApplication.Host.UseSerilog();

            webApplication.Services.AddControllers(options =>
            {
                options.Filters.Add<CustomActionFilterAttribute>();
                options.Filters.Add<GlobalExceptionFilterAttribute>();
            });

            webApplication.Services.AddFacade();
            webApplication.Services.AddPersistence(webApplication.Configuration);
            webApplication.Services.AddServices();
            webApplication.Services.AddAutoMapper();

            webApplication.Services.AddEndpointsApiExplorer();
            webApplication.Services.AddSwaggerGen();

            webApplication.Services.AddKafka(webApplication.Configuration, Log.Logger);

            webApplication.Services.AddApplicationInsightsTelemetry();

            try
            {
                var configuration = ConfigurationOptions.Parse(webApplication.Configuration["redis:hostname"], true);
                configuration.ResolveDns = true;
                webApplication.Services.AddSingleton<IConnectionMultiplexer>(cm => ConnectionMultiplexer.Connect(configuration));
            }
            catch (Exception)
            {
                Log.Logger.Error("No se encontro Redis");
            }

            return webApplication.Build();
        }

        /// <summary>
        /// Use application.
        /// </summary>
        /// <param name="app">WebApplicationBuilder.</param>
        /// <returns>WebApplication.</returns>
        public static WebApplication UseApplication(this WebApplication app)
        {
            app.UseSwagger();
            app.UseSwaggerUI();
            app.UseHttpsRedirection();
            app.UseAuthorization();
            app.MapControllers();
            return app;
        }
    }
}
