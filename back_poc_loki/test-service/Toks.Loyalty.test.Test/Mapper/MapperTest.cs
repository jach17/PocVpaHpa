// <summary>
// <copyright file="MapperTest.cs" company="Axity">
// This source code is Copyright Axity and MAY NOT be copied, reproduced,
// published, distributed or transmitted to or stored in any manner without prior
// written consent from Axity (www.axity.com).
// </copyright>
// </summary>

namespace Toks.Loyalty.test.Test.Mapper
{
    /// <summary>
    /// Class ProjectServiceTest.
    /// </summary>
    [TestFixture]
    public class MapperTest
    {
        /// <summary>
        /// Validate if mapper configuration is valid.
        /// </summary>
        [Test]
        public void ValidateMapperConfig()
        {
            var mappingConfig = new MapperConfiguration(mc => { mc.AddProfile(new AutoMapperProfile()); });

            // mappingConfig.AssertConfigurationIsValid();
            IMapper mapper = mappingConfig.CreateMapper();

            var fecha = "2024-06-25T00:00:00.000";
            Type typeDateType = typeof(DateTime);

            var result = mapper.Map<DateTime>(fecha);
            Type typeDateType2 = result.GetType();
            Assert.AreEqual(typeDateType, typeDateType2);
        }
    }
}
