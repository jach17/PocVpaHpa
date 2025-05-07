// <summary>
// <copyright file="UserServiceTest.cs" company="Axity">
// This source code is Copyright Axity and MAY NOT be copied, reproduced,
// published, distributed or transmitted to or stored in any manner without prior
// written consent from Axity (www.axity.com).
// </copyright>
// </summary>

namespace Toks.Loyalty.test.Test.Services
{
    /// <summary>
    /// Class ProjectServiceTest.
    /// </summary>
    [TestFixture]
    public class UserServiceTest : BaseTest
    {        
        private IMapper mapper;
        private DatabaseContext context;

        /// <summary>
        /// Init configuration.
        /// </summary>
        [OneTimeSetUp]
        public void Init()
        {
            var mapperConfiguration = new MapperConfiguration(cfg => cfg.AddProfile<AutoMapperProfile>());
            this.mapper = mapperConfiguration.CreateMapper();

            DbConnection connection = new SqliteConnection("Data Source=TempProject;Mode=Memory;Cache=Shared");
            connection.Open();
            var options = new DbContextOptionsBuilder<DatabaseContext>()
            .UseSqlite(connection).Options;

            this.context = new DatabaseContext(options);
            this.context.Database.EnsureDeleted();
            this.context.Database.EnsureCreated();
            this.context.SaveChanges();
        }
    }
}
